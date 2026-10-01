"""Generic deterministic search primitives."""
from __future__ import annotations
from collections import deque
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")

def breadth_first(start: T, expand: Callable[[T], Iterable[T]], goal: Callable[[T], bool]) -> T | None:
    queue = deque([start])
    seen: set[T] = {start}
    while queue:
        current = queue.popleft()
        if goal(current):
            return current
        for child in expand(current):
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return None
