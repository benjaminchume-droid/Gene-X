"""Priority-aware task queue built on Gene's task objects."""
from __future__ import annotations
import heapq
from dataclasses import dataclass, field
from .task import Task

@dataclass(order=True)
class _Queued:
    priority: float
    sequence: int
    task: Task = field(compare=False)

class TaskQueue:
    def __init__(self) -> None:
        self._heap: list[_Queued] = []
        self._sequence = 0

    def push(self, task: Task, priority: float = 0.0) -> None:
        self._sequence += 1
        heapq.heappush(self._heap, _Queued(priority, self._sequence, task))

    def pop(self) -> Task:
        if not self._heap:
            raise IndexError("task queue is empty")
        return heapq.heappop(self._heap).task

    def __len__(self) -> int:
        return len(self._heap)
