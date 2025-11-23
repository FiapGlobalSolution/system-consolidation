"""Azure Function entry points."""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any, Iterable
from uuid import uuid4

import azure.functions as func
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusError

from persistence import mongo_persistence
from sns_notifications import sns_notifier
from sqs_replication import sqs_replicator

app = func.FunctionApp()


class ServiceBusConfigError(RuntimeError):
	"""Raised when required Service Bus settings are absent."""


def _get_env_setting(key: str) -> str:
	value = os.environ.get(key)
	if not value:
		raise ServiceBusConfigError(f"Missing environment variable: {key}")
	return value


def _deserialize_message(message: ServiceBusMessage) -> tuple[Any | str, str]:
	body_bytes = b"".join(message.body)
	text = body_bytes.decode("utf-8", errors="replace")
	try:
		return json.loads(text), text
	except json.JSONDecodeError:
		return text, text



def _normalize_application_properties(props: Any) -> dict[str, Any] | None:
	if not props:
		return None
	if isinstance(props, dict):
		return {
			(_decode_key(key)): value
			for key, value in props.items()
		}
	return props  # leave as-is when type unsupported but JSON-safe


def _decode_key(key: Any) -> str:
	if isinstance(key, bytes):
		return key.decode("utf-8", errors="replace")
	return str(key)


def _build_document(
	queue_name: str,
	msg: ServiceBusMessage,
	payload: Any | str,
	raw_text: str,
	application_properties: Any,
) -> dict[str, Any]:
	metadata = {
		"message_id": msg.message_id,
		"delivery_count": msg.delivery_count,
		"sequence_number": msg.sequence_number,
		"enqueued_time_utc": msg.enqueued_time_utc.isoformat()
		if msg.enqueued_time_utc
		else None,
		"dead_letter_source": msg.dead_letter_source,
		"content_type": msg.content_type,
		"correlation_id": msg.correlation_id,
		"queue_name": queue_name,
	}

	document: dict[str, Any] = {
		"_id": msg.message_id or f"{queue_name}-{msg.sequence_number}-{uuid4().hex}",
		"queueName": queue_name,
		"metadata": metadata,
		"receivedAtUtc": datetime.now(timezone.utc).isoformat(),
		"applicationProperties": _normalize_application_properties(application_properties),
	}

	if isinstance(payload, str):
		document["payloadText"] = raw_text
	else:
		document["payload"] = payload

	partition_hint = None
	if isinstance(application_properties, dict):
		partition_hint = application_properties.get("partitionKey") or application_properties.get(
			"tenantId"
		)
	if isinstance(payload, dict) and not partition_hint:
		partition_hint = payload.get("tenantId") or payload.get("deviceId")

	partition_fallback = (
		partition_hint
		or metadata["message_id"]
		or (metadata["sequence_number"] and str(metadata["sequence_number"]))
		or queue_name
	)
	mongo_persistence.ensure_partition_key(document, partition_fallback)
	return document




def _process_messages(messages: Iterable[ServiceBusMessage], queue_name: str) -> None:
	should_persist = mongo_persistence.is_enabled()
	should_replicate = sqs_replicator.is_enabled()
	should_notify = sns_notifier.is_enabled()
	documents: list[dict[str, Any]] = []
	replication_docs: list[dict[str, Any]] = []
	for msg in messages:
		payload, raw_text = _deserialize_message(msg)
		metadata = {
			"message_id": msg.message_id,
			"delivery_count": msg.delivery_count,
			"sequence_number": msg.sequence_number,
			"enqueued_time_utc": msg.enqueued_time_utc.isoformat()
			if msg.enqueued_time_utc
			else None,
			"dead_letter_source": msg.dead_letter_source,
			"content_type": msg.content_type,
			"correlation_id": msg.correlation_id,
		}
		logging.info("Service Bus message received: %s", metadata)
		if isinstance(payload, str):
			logging.info("Message payload (text): %s", raw_text)
		else:
			logging.info("Message payload (JSON): %s", payload)

		# TODO: replace with domain-specific business logic.
		application_properties = getattr(msg, "application_properties", None)
		if application_properties is None:
			application_properties = getattr(msg, "user_properties", None)
		normalized_properties = _normalize_application_properties(application_properties)
		logging.debug("Application properties: %s", normalized_properties)
		if should_persist or should_replicate or should_notify:
			doc = _build_document(
				queue_name=queue_name,
				msg=msg,
				payload=payload,
				raw_text=raw_text,
				application_properties=normalized_properties,
			)
			if should_persist:
				documents.append(doc)
			if should_replicate:
				replication_docs.append(doc)
			if should_notify:
				sns_notifier.maybe_notify(doc)

	if documents:
		mongo_persistence.persist_documents(documents)
	if replication_docs:
		sqs_replicator.replicate(replication_docs)


@app.schedule(
	schedule="0 */5 * * * *",  # every 5 minutes
	arg_name="timer",
	run_on_startup=False,
	use_monitor=True,
)
def timer_drain_servicebus(timer: func.TimerRequest) -> None:
	"""Timer-triggered job that polls a Service Bus queue and processes messages."""

	try:
		connection = _get_env_setting("SERVICEBUS_CONNECTION")
		queue_name = _get_env_setting("SERVICEBUS_QUEUE_NAME")
	except ServiceBusConfigError as exc:
		logging.error("Service Bus configuration missing: %s", exc)
		return

	client = ServiceBusClient.from_connection_string(connection, logging_enable=True)
	max_message_count = int(os.environ.get("SERVICEBUS_MAX_MESSAGE_COUNT", "25"))
	max_wait_time = int(os.environ.get("SERVICEBUS_MAX_WAIT_TIME", "5"))

	schedule_status = getattr(timer, "schedule_status", None)
	last_fired = None
	if schedule_status:
		# schedule_status may arrive as a simple namespace or as a dict depending on the worker version.
		last_fired = getattr(schedule_status, "last", None)
		if last_fired is None and isinstance(schedule_status, dict):
			last_fired = schedule_status.get("last")

	logging.info(
		"Timer firing at %s. Polling queue '%s' (max_count=%s, wait=%ss)",
		last_fired,
		queue_name,
		max_message_count,
		max_wait_time,
	)

	try:
		with client.get_queue_receiver(queue_name=queue_name, max_wait_time=max_wait_time) as receiver:
			received = receiver.receive_messages(
				max_message_count=max_message_count,
				max_wait_time=max_wait_time,
			)

			if not received:
				logging.info("No messages available in queue '%s'", queue_name)
				return

			_process_messages(received, queue_name=queue_name)

			for msg in received:
				receiver.complete_message(msg)
				logging.debug("Completed message %s", msg.message_id)

	except ServiceBusError as exc:
		logging.exception("Service Bus receive failed: %s", exc)
	finally:
		client.close()

