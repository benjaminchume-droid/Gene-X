"""Dynamic working-context buckets.

Buckets are retrieval units, not a single monolithic context window.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic
from typing import Any


@dataclass
class ContextBucket:
    bucket_id: str
    capacity: int = 64
    priority: float = 0.0
    items: list[Any] = field(default_factory=list)
    last_access: float = field(default_factory=monotonic)

    def add(self, item: Any) -> None:
        if self.capacity < 1:
            raise ValueError("capacity must be positive")
        self.items.append(item)
        self.last_access = monotonic()
        if len(self.items) > self.capacity:
            self.items.pop(0)

    def touch(self) -> None:
        self.last_access = monotonic()

    def score(self) -> float:
        age = max(0.0, monotonic() - self.last_access)
        return self.priority / (1.0 + age)


@dataclass
class ContextStore:
    """Collection of independently addressable working-memory regions."""

    buckets: dict[str, ContextBucket] = field(default_factory=dict)

    def ensure(self, bucket_id: str, *, capacity: int = 64, priority: float = 0.0) -> ContextBucket:
        bucket = self.buckets.get(bucket_id)
        if bucket is None:
            bucket = ContextBucket(bucket_id, capacity, priority)
            self.buckets[bucket_id] = bucket
        return bucket

    def add(self, bucket_id: str, item: Any, *, capacity: int = 64, priority: float = 0.0) -> None:
        self.ensure(bucket_id, capacity=capacity, priority=priority).add(item)

    def retrieve(self, limit: int = 4) -> list[ContextBucket]:
        return sorted(self.buckets.values(), key=lambda b: b.score(), reverse=True)[:limit]
