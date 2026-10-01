"""Bounded working-memory view over the persistent memory substrate."""
from __future__ import annotations
from collections import deque
from typing import Any

class WorkingMemory:
    def __init__(self, capacity: int = 64) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._items: deque[Any] = deque(maxlen=capacity)

    def add(self, item: Any) -> None:
        self._items.append(item)

    def items(self) -> tuple[Any, ...]:
        return tuple(self._items)

    def clear(self) -> None:
        self._items.clear()
