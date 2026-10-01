"""Watchdog for detecting stalled work."""
from __future__ import annotations
from dataclasses import dataclass
from time import monotonic

@dataclass
class Watch:
    work_id: str
    timeout_seconds: float
    last_progress: float

    @classmethod
    def create(cls, work_id: str, timeout_seconds: float) -> "Watch":
        if timeout_seconds <= 0:
            raise ValueError("timeout must be positive")
        return cls(work_id, timeout_seconds, monotonic())

    def progress(self) -> None:
        self.last_progress = monotonic()

    def stalled(self) -> bool:
        return monotonic() - self.last_progress >= self.timeout_seconds
