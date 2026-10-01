"""ETA estimation from observed task durations."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DurationEstimate:
    samples: int = 0
    total_seconds: float = 0.0

    @property
    def average_seconds(self) -> float | None:
        return self.total_seconds / self.samples if self.samples else None

    def observe(self, seconds: float) -> None:
        if seconds < 0:
            raise ValueError("duration cannot be negative")
        self.samples += 1
        self.total_seconds += seconds

    def estimate(self, remaining: int) -> float | None:
        average = self.average_seconds
        return None if average is None else average * max(0, remaining)
