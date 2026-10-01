"""Simple deterministic indexes over memory records."""
from __future__ import annotations
from collections import defaultdict
from typing import Hashable

class MemoryIndex:
    def __init__(self) -> None:
        self._index: dict[Hashable, set[str]] = defaultdict(set)

    def add(self, key: Hashable, record_id: str) -> None:
        self._index[key].add(record_id)

    def remove(self, key: Hashable, record_id: str) -> None:
        bucket = self._index.get(key)
        if not bucket:
            return
        bucket.discard(record_id)
        if not bucket:
            self._index.pop(key, None)

    def lookup(self, key: Hashable) -> tuple[str, ...]:
        return tuple(self._index.get(key, ()))
