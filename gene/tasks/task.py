"""General-purpose task representation."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

class TaskStatus(StrEnum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"

@dataclass(slots=True)
class Task:
    objective: str
    task_id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    dependencies: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    error: str | None = None

    def ready(self, completed: set[str]) -> bool:
        return self.status in {TaskStatus.PENDING, TaskStatus.READY} and self.dependencies <= completed
