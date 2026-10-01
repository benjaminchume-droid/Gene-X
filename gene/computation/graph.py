"""Small graph data structure for exact graph reasoning."""
from __future__ import annotations
from collections import defaultdict
from typing import Hashable

class Graph:
    def __init__(self) -> None:
        self._edges: dict[Hashable, set[Hashable]] = defaultdict(set)

    def connect(self, source: Hashable, target: Hashable, *, directed: bool = True) -> None:
        self._edges[source].add(target)
        if not directed:
            self._edges[target].add(source)

    def neighbors(self, node: Hashable) -> frozenset[Hashable]:
        return frozenset(self._edges.get(node, ()))

    def nodes(self) -> frozenset[Hashable]:
        return frozenset(self._edges)
