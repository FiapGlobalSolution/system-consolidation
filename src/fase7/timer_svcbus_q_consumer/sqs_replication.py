"""Optional Amazon SQS replication helpers."""

from __future__ import annotations

import json
import logging
import os
from itertools import islice
from threading import Lock
from typing import Iterable, List
from uuid import uuid4

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _to_bool(value: str | None) -> bool:
	return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _take(chunk_size: int, iterator: Iterable[dict]) -> list[dict]:
	return list(islice(iterator, chunk_size))


class SQSReplicator:
	"""Sends JSON events to an Amazon SQS queue when enabled."""

	def __init__(self) -> None:
		self._enabled = _to_bool(os.getenv("SQS_ENABLED"))
		self._queue_url = os.getenv("SQS_QUEUE_URL")
		self._region = os.getenv("AWS_REGION")
		self._access_key = os.getenv("AWS_ACCESS_KEY_ID")
		self._secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
		self._session_token = os.getenv("AWS_SESSION_TOKEN")
		self._batch_size = int(os.getenv("SQS_BATCH_SIZE", "10"))
		self._max_retries = int(os.getenv("SQS_MAX_RETRIES", "3"))
		self._client = None
		self._lock = Lock()

	def is_enabled(self) -> bool:
		return all([self._enabled, self._queue_url, self._region, self._access_key, self._secret_key])

	def _get_client(self):
		if self._client:
			return self._client
		with self._lock:
			if self._client:
				return self._client
			self._client = boto3.client(
				"sqs",
				region_name=self._region,
				aws_access_key_id=self._access_key,
				aws_secret_access_key=self._secret_key,
				aws_session_token=self._session_token,
			)
			return self._client

	def replicate(self, documents: Iterable[dict]) -> None:
		if not self.is_enabled():
			logging.debug("SQS replication disabled or misconfigured; skipping send")
			return

		iterator = iter(documents)
		while True:
			batch = _take(self._batch_size, iterator)
			if not batch:
				break
			self._send_batch(batch)

	def _send_batch(self, batch: List[dict]) -> None:
		client = self._get_client()
		attempt = 0
		entries = [
			{
				"Id": doc.get("_id") or uuid4().hex,
				"MessageBody": json.dumps(doc, default=str),
			}
			for doc in batch
		]

		remaining = entries
		while remaining and attempt < self._max_retries:
			attempt += 1
			try:
				response = client.send_message_batch(
					QueueUrl=self._queue_url,
					Entries=remaining,
				)
				failed_ids = {item["Id"] for item in response.get("Failed", [])}
				if not failed_ids:
					logging.info(
						"Replicated %s event(s) to SQS queue %s", len(remaining), self._queue_url
					)
					return
				remaining = [entry for entry in remaining if entry["Id"] in failed_ids]
				logging.warning(
					"SQS batch send partially failed (attempt %s/%s). Retrying %s message(s)",
					attempt,
					self._max_retries,
					len(remaining),
				)
			except (BotoCoreError, ClientError) as exc:
				logging.warning(
					"SQS batch send failed (attempt %s/%s): %s",
					attempt,
					self._max_retries,
					exc,
				)
				if attempt == self._max_retries:
					break

		if remaining:
			logging.error(
				"Failed to replicate %s event(s) to SQS after %s attempts", len(remaining), self._max_retries
			)


sqs_replicator = SQSReplicator()

__all__ = ["sqs_replicator", "SQSReplicator"]
