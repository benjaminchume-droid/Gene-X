"""Dependency graph for persistent work."""
from __future__ import annotations

from .task import Task, TaskStatus

class TaskGraph:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}

    def add(self, task: Task) -> Task:
        if task.task_id in self.tasks:
            raise ValueError(f"task already exists: {task.task_id}")
        if task.task_id in task.dependencies:
            raise ValueError("task cannot depend on itself")
        self.tasks[task.task_id] = task
        return task

    def completed(self) -> set[str]:
        return {i for i, t in self.tasks.items() if t.status is TaskStatus.SUCCEEDED}

    def ready(self) -> list[Task]:
        done = self.completed()
        return [t for t in self.tasks.values() if t.ready(done)]

    def mark(self, task_id: str, status: TaskStatus, *, result=None, error=None) -> None:
        task = self.tasks[task_id]
        task.status = status
        task.result = result
        task.error = error
