"""Planning primitives over task graphs and explicit actions."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from gene.tasks.graph import TaskGraph

@dataclass(frozen=True)
class Action:
    name: str
    execute: Callable[..., Any]

class Planner:
    def __init__(self, graph: TaskGraph) -> None:
        self.graph = graph

    def ready_tasks(self) -> list[Any]:
        return self.graph.ready()

    def run_ready(self, actions: dict[str, Action]) -> list[Any]:
        results = []
        for task in self.graph.ready():
            action = actions.get(task.task_id)
            if action is None:
                continue
            self.graph.mark(task.task_id, "RUNNING")
            try:
                task.result = action.execute(task)
                self.graph.mark(task.task_id, "SUCCEEDED")
                results.append(task.result)
            except Exception as exc:
                task.error = str(exc)
                self.graph.mark(task.task_id, "FAILED")
        return results
