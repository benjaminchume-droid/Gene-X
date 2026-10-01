"""Explicit priority model for competing objectives."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Priority:
    urgency: float = 0.0
    importance: float = 0.0
    dependency_pressure: float = 0.0

    @property
    def score(self) -> float:
        return self.urgency + self.importance + self.dependency_pressure
