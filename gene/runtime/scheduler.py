"""Resource-aware scheduling of independent work."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from .resources import ResourceUsage, ResourceLimits

@dataclass(order=True)
class ScheduledWork:
    priority: float
    work_id: str = field(compare=False)
    operation: Callable[[], Any] = field(compare=False)
    estimated_usage: ResourceUsage = field(default_factory=ResourceUsage, compare=False)

class Scheduler:
    def __init__(self, limits: ResourceLimits | None = None) -> None:
        self.limits = limits
        self._queue: list[ScheduledWork] = []

    def submit(self, work: ScheduledWork) -> None:
        if self.limits and not self.limits.allows(work.estimated_usage):
            raise MemoryError(f"work exceeds runtime resource limits: {work.work_id}")
        self._queue.append(work)
        self._queue.sort(reverse=True)

    def next(self) -> ScheduledWork | None:
        return self._queue.pop(0) if self._queue else None

    def pending(self) -> tuple[ScheduledWork, ...]:
        return tuple(self._queue)
