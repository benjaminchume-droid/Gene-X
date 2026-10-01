"""Generic deterministic search primitives."""
from __future__ import annotations
from collections import deque
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")

def breadth_first(start: T, expand: Callable[[T], Iterable[T]], goal: Callable[[T], bool]) -> T | None:
    queue: deque[T] = deque([start])
    seen: set[T] = {start}
    while queue:
        node = queue.popleft()
        if goal(node):
            return node
        for child in expand(node):
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return None
