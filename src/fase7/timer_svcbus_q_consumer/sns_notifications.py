"""Optional AWS SNS notifications for environmental alerts."""

from __future__ import annotations

import json
import logging
import os
from threading import Lock
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def _to_bool(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def _to_float(value: Any) -> float | None:
    try:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        return float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        return None


class SNSNotifier:
    """Evaluates payloads and publishes alerts to an SNS topic."""

    def __init__(self) -> None:
        self._enabled = _to_bool(os.getenv("SNS_ENABLED"))
        self._topic_arn = os.getenv("SNS_TOPIC_ARN")
        self._subject = os.getenv("SNS_SUBJECT", "IoT Environmental Alert")
        self._humidity_threshold = float(os.getenv("SNS_MIN_HUMIDITY", "20"))
        self._temperature_threshold = float(os.getenv("SNS_MAX_TEMPERATURE", "32"))
        self._region = os.getenv("AWS_REGION")
        self._access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self._secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self._session_token = os.getenv("AWS_SESSION_TOKEN")
        self._max_retries = int(os.getenv("SNS_MAX_RETRIES", "3"))
        self._client = None
        self._lock = Lock()

    def is_enabled(self) -> bool:
        return all([
            self._enabled,
            self._topic_arn,
            self._region,
            self._access_key,
            self._secret_key,
        ])

    def _get_client(self):
        if self._client:
            return self._client
        with self._lock:
            if self._client:
                return self._client
            self._client = boto3.client(
                "sns",
                region_name=self._region,
                aws_access_key_id=self._access_key,
                aws_secret_access_key=self._secret_key,
                aws_session_token=self._session_token,
            )
            return self._client

    def maybe_notify(self, document: dict[str, Any]) -> None:
        if not self.is_enabled():
            return

        payload = document.get("payload")
        if payload is None and isinstance(document.get("payloadText"), str):
            payload = self._try_parse(document["payloadText"])

        if not isinstance(payload, dict):
            return

        humidity = self._extract_metric(payload, ["humidity", "humidade"])
        temperature = self._extract_metric(payload, ["temperature", "temperatura"])

        reasons: list[str] = []
        if humidity is not None and humidity < self._humidity_threshold:
            reasons.append(f"Humidity {humidity}% below {self._humidity_threshold}%")
        if temperature is not None and temperature > self._temperature_threshold:
            reasons.append(f"Temperature {temperature}°C above {self._temperature_threshold}°C")

        if not reasons:
            return

        alert = {
            "reasons": reasons,
            "humidity": humidity,
            "temperature": temperature,
            "queueName": document.get("queueName"),
            "messageId": document.get("metadata", {}).get("message_id"),
            "receivedAtUtc": document.get("receivedAtUtc"),
            "payload": payload,
        }

        self._publish(alert)

    def _publish(self, alert: dict[str, Any]) -> None:
        client = self._get_client()
        attempt = 0
        while attempt < self._max_retries:
            attempt += 1
            try:
                client.publish(
                    TopicArn=self._topic_arn,
                    Subject=self._subject,
                    Message=json.dumps(alert, default=str),
                )
                logging.info("Published SNS alert to %s", self._topic_arn)
                return
            except (BotoCoreError, ClientError) as exc:
                logging.warning(
                    "SNS publish failed (attempt %s/%s): %s",
                    attempt,
                    self._max_retries,
                    exc,
                )
        logging.error("Failed to publish SNS alert after %s attempts", self._max_retries)

    @staticmethod
    def _try_parse(raw: str) -> dict[str, Any] | None:
        try:
            candidate = json.loads(raw)
            return candidate if isinstance(candidate, dict) else None
        except json.JSONDecodeError:
            return None

    @staticmethod
    def _extract_metric(payload: dict[str, Any], keys: list[str]) -> float | None:
        for key in keys:
            if key in payload:
                return _to_float(payload[key])
        return None


sns_notifier = SNSNotifier()

__all__ = ["sns_notifier", "SNSNotifier"]
