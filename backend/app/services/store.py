from datetime import datetime
from typing import Any


class InMemoryStore:
    def __init__(self) -> None:
        self.image_metadata: list[dict[str, Any]] = []
        self.claims: dict[str, dict[str, Any]] = {}
        self.audit_queue: list[dict[str, Any]] = []


store = InMemoryStore()


def save_metadata(payload: dict[str, Any]) -> dict[str, Any]:
    record = {
        **payload,
        "created_at": datetime.utcnow().isoformat(),
    }
    store.image_metadata.append(record)
    return record


def create_claim(payload: dict[str, Any]) -> dict[str, Any]:
    record = {
        **payload,
        "status": "submitted",
        "created_at": datetime.utcnow().isoformat(),
    }
    store.claims[payload["claim_id"]] = record
    return record


def add_audit_flag(payload: dict[str, Any]) -> None:
    store.audit_queue.append(payload)


def list_audit_queue() -> list[dict[str, Any]]:
    return store.audit_queue
