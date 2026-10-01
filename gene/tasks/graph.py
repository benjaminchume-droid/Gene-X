"""Directed task graph with dependency-aware readiness."""
from __future__ import annotations
from .task import Task

class TaskGraph:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}

    def add(self, task: Task) -> None:
        if task.task_id in self.tasks:
            raise ValueError(f"duplicate task: {task.task_id}")
        self.tasks[task.task_id] = task

    def completed(self) -> set[str]:
        return {task.task_id for task in self.tasks.values() if task.status.value == "succeeded"}

    def ready(self) -> list[Task]:
        done = self.completed()
        return [task for task in self.tasks.values() if task.ready(done)]

    def mark(self, task_id: str, status: str) -> None:
        task = self.tasks[task_id]
        from .task import TaskStatus
        task.status = TaskStatus(status)
