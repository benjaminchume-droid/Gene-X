"""Domain-neutral spatial primitives."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    coordinates: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.coordinates:
            raise ValueError("a point needs at least one dimension")


@dataclass(frozen=True, slots=True)
class SpatialRelation:
    first: str
    relation: str
    second: str
    confidence: float = 1.0
