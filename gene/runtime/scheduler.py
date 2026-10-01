"""Cooperative scheduler with explicit priorities and cancellation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from ..tasks.queue import TaskQueue
from ..tasks.task import Task


@dataclass(slots=True)
class ScheduledJob:
    task: Task
    operation: Callable[[], object]
    cancelled: bool = False


@dataclass
class Scheduler:
    queue: TaskQueue = field(default_factory=TaskQueue)
    jobs: dict[str, ScheduledJob] = field(default_factory=dict)

    def submit(self, job: Callable[[], object], task: Task, priority: float = 0.0) -> str:
        scheduled = ScheduledJob(task, job)
        self.jobs[task.task_id] = scheduled
        self.queue.push(task, priority)
        return task.task_id

    def cancel(self, task_id: str) -> bool:
        scheduled = self.jobs.get(task_id)
        if scheduled is None:
            return False
        scheduled.cancelled = True
        return True

    def run_ready(self, limit: int | None = None) -> int:
        count = 0
        while len(self.queue) and (limit is None or count < limit):
            task = self.queue.pop()
            scheduled = self.jobs.get(task.task_id)
            if scheduled is None or scheduled.cancelled:
                continue
            scheduled.operation()
            count += 1
        return count
