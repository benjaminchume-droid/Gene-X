"""Temporal primitives independent of language or a fixed clock resolution."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Interval:
    start: datetime
    end: datetime | None = None

    def __post_init__(self) -> None:
        if self.end is not None and self.end < self.start:
            raise ValueError("interval end cannot precede start")

    @property
    def open_ended(self) -> bool:
        return self.end is None


@dataclass(frozen=True, slots=True)
class TemporalRelation:
    first: str
    relation: str
    second: str
    confidence: float = 1.0
