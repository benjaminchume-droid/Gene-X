"""Learning consolidation: convert evaluated experience into durable knowledge."""
from __future__ import annotations
from typing import Any, Callable, Iterable

class LearningConsolidator:
    def __init__(self, commit: Callable[[Iterable[Any]], Any]) -> None:
        self.commit = commit

    def consolidate(self, experiences: Iterable[Any]) -> Any:
        return self.commit(tuple(experiences))
