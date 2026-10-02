"""Learned, domain-neutral memory retrieval primitives."""
from __future__ import annotations
from dataclasses import dataclass
from math import sqrt
from typing import Any, Callable, Iterable
from .store import MemoryRecord, MemoryStore

@dataclass(frozen=True, slots=True)
class Retrieval:
    record: MemoryRecord
    score: float

class MemoryRetriever:
    """Retrieve memories by a supplied representation function.

    The retriever does not know any vocabulary or domain. Callers decide how
    an observation becomes a vector; the index only performs similarity.
    """
    def __init__(self, store: MemoryStore, encode: Callable[[Any], Iterable[float]]) -> None:
        self.store = store
        self.encode = encode

    @staticmethod
    def cosine(a: Iterable[float], b: Iterable[float]) -> float:
        left, right = tuple(a), tuple(b)
        if len(left) != len(right):
            raise ValueError("vectors must have equal length")
        aa = sqrt(sum(x*x for x in left)); bb = sqrt(sum(x*x for x in right))
        if aa == 0 or bb == 0:
            return 0.0
        return sum(x*y for x,y in zip(left,right)) / (aa*bb)

    def query(self, value: Any, *, limit: int = 8, kinds: set[str] | None = None) -> tuple[Retrieval, ...]:
        if limit < 1:
            return ()
        q = self.encode(value)
        scored = []
        for record in self.store.records():
            if kinds is not None and record.kind not in kinds:
                continue
            scored.append(Retrieval(record, self.cosine(q, self.encode(record.value))))
        scored.sort(key=lambda item: item.score, reverse=True)
        return tuple(scored[:limit])
