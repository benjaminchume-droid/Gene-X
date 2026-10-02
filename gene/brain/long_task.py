"""Durable long-running task state.

An objective is the durable intention. A task is one current execution step.
The plan can therefore change while the objective survives.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4


class LongTaskState(StrEnum):
    PLANNING = "planning"
    RUNNING = "running"
    WAITING = "waiting"
    RECOVERING = "recovering"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass(slots=True)
class WorkItem:
    description: str
    work_id: str = field(default_factory=lambda: str(uuid4()))
    dependencies: set[str] = field(default_factory=set)
    status: LongTaskState = LongTaskState.PLANNING
    attempts: int = 0
    result: Any = None
    error: str | None = None


@dataclass
class LongTaskController:
    """Maintains a mutable execution graph for a durable objective."""

    objective_id: str
    items: dict[str, WorkItem] = field(default_factory=dict)
    state: LongTaskState = LongTaskState.PLANNING
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_work(self, description: str, *, dependencies: set[str] | None = None) -> WorkItem:
        item = WorkItem(description, dependencies=set(dependencies or ()))
        self.items[item.work_id] = item
        return item

    def ready(self) -> list[WorkItem]:
        completed = {i.work_id for i in self.items.values() if i.status == LongTaskState.COMPLETED}
        return [i for i in self.items.values()
                if i.status == LongTaskState.PLANNING and i.dependencies <= completed]

    def amend(self, description: str, *, dependencies: set[str] | None = None) -> WorkItem:
        """Add work without replacing the existing objective or work graph."""
        return self.add_work(description, dependencies=dependencies)

    def begin(self) -> None:
        if self.state in {LongTaskState.PLANNING, LongTaskState.WAITING, LongTaskState.RECOVERING}:
            self.state = LongTaskState.RUNNING

    def complete(self, work_id: str, result: Any = None) -> None:
        item = self.items[work_id]
        item.status = LongTaskState.COMPLETED
        item.result = result
        self.state = LongTaskState.COMPLETED if self.items and all(
            i.status == LongTaskState.COMPLETED for i in self.items.values()
        ) else LongTaskState.RUNNING

    def fail(self, work_id: str, error: str) -> None:
        item = self.items[work_id]
        item.attempts += 1
        item.error = error
        item.status = LongTaskState.RECOVERING
        self.state = LongTaskState.RECOVERING
