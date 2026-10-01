"""Dependency primitives for dynamically evolving work graphs."""
from __future__ import annotations
from collections import defaultdict

class DependencyGraph:
    def __init__(self) -> None:
        self._dependencies: dict[str, set[str]] = defaultdict(set)

    def require(self, task_id: str, dependency_id: str) -> None:
        if task_id == dependency_id:
            raise ValueError("task cannot depend on itself")
        self._dependencies[task_id].add(dependency_id)

    def dependencies(self, task_id: str) -> frozenset[str]:
        return frozenset(self._dependencies.get(task_id, ()))

    def ready(self, task_id: str, completed: set[str]) -> bool:
        return self.dependencies(task_id).issubset(completed)
