"""Feedback primitives independent of any particular learning algorithm."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Feedback:
    score: float | None = None
    correction: Any = None
    reason: str = ""

    def __post_init__(self) -> None:
        if self.score is not None and not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0 and 1")
