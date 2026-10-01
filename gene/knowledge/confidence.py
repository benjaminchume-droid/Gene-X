"""Confidence utilities with bounded values."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Confidence:
    value: float
    basis: str = ""

    def __post_init__(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

def combine(values: list[Confidence]) -> Confidence:
    if not values:
        raise ValueError("cannot combine empty confidence list")
    return Confidence(sum(v.value for v in values) / len(values), "mean")
