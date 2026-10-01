"""Deterministic graph primitives."""
from __future__ import annotations
from collections import defaultdict, deque
from typing import Hashable

class Graph:
    def __init__(self, directed: bool = True) -> None:
        self.directed = directed
        self._edges: dict[Hashable, set[Hashable]] = defaultdict(set)

    def add_edge(self, source: Hashable, target: Hashable) -> None:
        self._edges[source].add(target)
        if not self.directed:
            self._edges[target].add(source)

    def neighbors(self, node: Hashable) -> frozenset[Hashable]:
        return frozenset(self._edges.get(node, ()))

    def reachable(self, source: Hashable) -> set[Hashable]:
        seen: set[Hashable] = set()
        queue = deque([source])
        while queue:
            node = queue.popleft()
            if node in seen:
                continue
            seen.add(node)
            queue.extend(self._edges.get(node, ()))
        return seen
