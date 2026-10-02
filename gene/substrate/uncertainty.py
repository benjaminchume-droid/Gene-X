"""Explicit uncertainty primitives."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Belief:
    proposition: Any
    confidence: float
    evidence: tuple[str, ...] = ()
    source: str | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


def combine_independent(confidences: list[float]) -> float:
    """Combine independent support without claiming certainty."""
    if any(not 0.0 <= c <= 1.0 for c in confidences):
        raise ValueError("confidences must be between 0 and 1")
    remaining = 1.0
    for confidence in confidences:
        remaining *= 1.0 - confidence
    return 1.0 - remaining
