"""Persistent supervisor for dependency-aware autonomous work."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Any

from ..tasks.graph import TaskGraph
from ..tasks.task import Task, TaskStatus
from ..tasks.queue import TaskQueue
from ..tasks.priorities import Priority
from .events import Event, EventBus


@dataclass(slots=True)
class TaskExecution:
    task_id: str
    value: Any = None
    error: Exception | None = None


@dataclass
class Supervisor:
    graph: TaskGraph = field(default_factory=TaskGraph)
    queue: TaskQueue = field(default_factory=TaskQueue)
    events: EventBus = field(default_factory=EventBus)
    executors: dict[str, Callable[[Task], Any]] = field(default_factory=dict)
    active: bool = False

    def add_task(self, task: Task, executor: Callable[[Task], Any], priority: Priority | None = None) -> None:
        self.graph.add(task)
        self.executors[task.task_id] = executor
        if task.ready(self.graph.completed()):
            task.status = TaskStatus.READY
            self.queue.push(task, priority.score() if priority else 0.0)
        self.events.publish(Event("task.added", {"task_id": task.task_id}))

    def refresh(self) -> int:
        queued = {item.task.task_id for item in self.queue._heap}
        count = 0
        for task in self.graph.ready():
            if task.task_id not in queued:
                task.status = TaskStatus.READY
                self.queue.push(task)
                count += 1
        return count

    def run_once(self) -> TaskExecution | None:
        self.refresh()
        if not len(self.queue):
            return None
        task = self.queue.pop()
        if not task.ready(self.graph.completed()):
            return None
        task.status = TaskStatus.RUNNING
        self.events.publish(Event("task.started", {"task_id": task.task_id}))
        try:
            value = self.executors[task.task_id](task)
        except Exception as exc:
            task.status = TaskStatus.FAILED
            task.error = str(exc)
            self.events.publish(Event("task.failed", {"task_id": task.task_id, "error": str(exc)}))
            return TaskExecution(task.task_id, error=exc)
        task.result = value
        task.status = TaskStatus.SUCCEEDED
        self.events.publish(Event("task.succeeded", {"task_id": task.task_id}))
        return TaskExecution(task.task_id, value=value)

    def run(self, max_steps: int | None = None) -> list[TaskExecution]:
        self.active = True
        results: list[TaskExecution] = []
        steps = 0
        try:
            while self.active and (max_steps is None or steps < max_steps):
                result = self.run_once()
                if result is None:
                    break
                results.append(result)
                steps += 1
        finally:
            self.active = False
        return results

    def stop(self) -> None:
        self.active = False

    def pending(self) -> list[Task]:
        return [task for task in self.graph.tasks.values()
                if task.status not in {TaskStatus.SUCCEEDED, TaskStatus.CANCELLED}]
