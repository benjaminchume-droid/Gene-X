"""Cooperative scheduler for runtime work."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

@dataclass(slots=True)
class Scheduler:
    jobs: list[Callable[[], None]] = field(default_factory=list)

    def submit(self, job: Callable[[], None]) -> None:
        self.jobs.append(job)

    def run_ready(self, limit: int | None = None) -> int:
        count = 0
        while self.jobs and (limit is None or count < limit):
            job = self.jobs.pop(0)
            job()
            count += 1
        return count
