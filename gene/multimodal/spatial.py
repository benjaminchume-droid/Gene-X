"""General spatial primitives usable across image, video and 3D."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Point:
    coordinates: tuple[float, ...]

@dataclass(frozen=True, slots=True)
class Bounds:
    minimum: tuple[float, ...]
    maximum: tuple[float, ...]

    def contains(self, point: Point) -> bool:
        return len(point.coordinates) == len(self.minimum) == len(self.maximum) and all(
            lo <= value <= hi
            for value, lo, hi in zip(point.coordinates, self.minimum, self.maximum)
        )
