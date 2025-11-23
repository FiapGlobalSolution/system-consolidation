"""Optional Cosmos DB (Mongo API) persistence helpers."""

from __future__ import annotations

import logging
import os
from threading import Lock
from typing import Iterable, Mapping, MutableMapping

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


def _to_bool(value: str | None) -> bool:
	return (value or "").strip().lower() in {"1", "true", "yes", "on"}


class MongoPersistence:
	"""Stores documents in Cosmos DB configured for the MongoDB API."""

	_client: MongoClient | None
	_collection: Collection | None

	def __init__(self) -> None:
		self._enabled = _to_bool(os.getenv("COSMOS_MONGO_ENABLED"))
		self._conn_str = os.getenv("COSMOS_MONGO_CONN_STRING")
		self._database = os.getenv("COSMOS_MONGO_DB")
		self._collection_name = os.getenv("COSMOS_MONGO_COLLECTION")
		self._partition_field = os.getenv("COSMOS_MONGO_PARTITION_FIELD", "partitionKey")
		self._client = None
		self._collection = None
		self._lock = Lock()

	def is_enabled(self) -> bool:
		return all(
			[
				self._enabled,
				self._conn_str,
				self._database,
				self._collection_name,
			]
		)

	def _get_collection(self) -> Collection:
		if self._collection:
			return self._collection

		with self._lock:
			if self._collection:
				return self._collection
			self._client = MongoClient(self._conn_str, appname="timer_svcbus_q_consumer")
			self._collection = self._client[self._database][self._collection_name]
			return self._collection

	def persist_documents(self, documents: Iterable[MutableMapping[str, object]]) -> None:
		if not self.is_enabled():
			logging.debug("Mongo persistence disabled or misconfigured; skipping insert")
			return

		docs = list(documents)
		if not docs:
			return

		try:
			collection = self._get_collection()
			collection.insert_many(docs, ordered=False)
			logging.info(
				"Persisted %s document(s) to Cosmos Mongo collection '%s'",
				len(docs),
				self._collection_name,
			)
		except PyMongoError as exc:
			logging.exception("Failed to persist documents to Cosmos Mongo: %s", exc)

	def ensure_partition_key(self, document: MutableMapping[str, object], fallback: str) -> None:
		if self._partition_field not in document:
			document[self._partition_field] = fallback


mongo_persistence = MongoPersistence()

__all__ = ["MongoPersistence", "mongo_persistence"]
