"""Spatial primitives shared by image, video and 3D."""
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class Point:
    coordinates: tuple[float, ...]
@dataclass(frozen=True, slots=True)
class Bounds:
    minimum: tuple[float, ...]
    maximum: tuple[float, ...]
    def contains(self, point):
        return len(point.coordinates)==len(self.minimum)==len(self.maximum) and all(lo <= value <= hi for value,lo,hi in zip(point.coordinates,self.minimum,self.maximum))
