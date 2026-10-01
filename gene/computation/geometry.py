"""Exact Euclidean geometry primitives."""
from __future__ import annotations
from dataclasses import dataclass
from math import hypot

@dataclass(frozen=True)
class Point:
    x: float
    y: float

    def distance(self, other: "Point") -> float:
        return hypot(self.x - other.x, self.y - other.y)

@dataclass(frozen=True)
class Segment:
    start: Point
    end: Point

    @property
    def length(self) -> float:
        return self.start.distance(self.end)

def midpoint(a: Point, b: Point) -> Point:
    return Point((a.x + b.x) / 2, (a.y + b.y) / 2)
