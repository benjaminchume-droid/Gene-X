"""Persistent-memory abstraction.

Storage mechanics are deliberately separated from memory semantics.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

@dataclass(frozen=True, slots=True)
class MemoryRecord:
    key: str
    value: Any
    kind: str = "general"
    metadata: dict[str, Any] = field(default_factory=dict)

class MemoryStore:
    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def put(self, record: MemoryRecord) -> None:
        self._records[record.key] = record

    def get(self, key: str) -> MemoryRecord | None:
        return self._records.get(key)

    def delete(self, key: str) -> None:
        self._records.pop(key, None)

    def records(self, kind: str | None = None) -> Iterable[MemoryRecord]:
        values = self._records.values()
        return tuple(r for r in values if kind is None or r.kind == kind)
