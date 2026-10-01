"""Video representation boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class VideoStream:
    frames: Any
    fps: float
    duration: float

    def __post_init__(self) -> None:
        if self.fps <= 0 or self.duration < 0:
            raise ValueError("invalid video timing")
