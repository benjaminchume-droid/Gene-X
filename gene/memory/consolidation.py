"""Memory consolidation hooks without assuming a particular learning algorithm."""
from __future__ import annotations
from typing import Any, Callable, Iterable

class Consolidator:
    def __init__(self, transform: Callable[[Iterable[Any]], Iterable[Any]]) -> None:
        self.transform = transform

    def consolidate(self, records: Iterable[Any]) -> list[Any]:
        return list(self.transform(records))
