"""Decompose goals into explicit task graph nodes."""
from __future__ import annotations
from typing import Iterable
from gene.tasks.task import Task
from gene.tasks.graph import TaskGraph

def decompose(objective: str, steps: Iterable[str]) -> TaskGraph:
    graph = TaskGraph()
    previous: str | None = None
    for description in steps:
        task = Task(objective=description)
        if previous:
            task.dependencies.add(previous)
        graph.add(task)
        previous = task.task_id
    return graph
