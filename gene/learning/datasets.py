"""Streaming training data primitives.

Datasets are streams of experiences, not necessarily token corpora.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import islice
from typing import Generic, Iterable, Iterator, TypeVar

X = TypeVar("X")
Y = TypeVar("Y")


@dataclass(frozen=True, slots=True)
class Sample(Generic[X, Y]):
    input: X
    target: Y
    metadata: dict[str, object] = field(default_factory=dict)


class Dataset(Generic[X, Y]):
    def __init__(self, samples: Iterable[Sample[X, Y]]) -> None:
        self._samples = samples

    def __iter__(self) -> Iterator[Sample[X, Y]]:
        yield from self._samples

    def batch(self, size: int) -> Iterator[list[Sample[X, Y]]]:
        if size < 1:
            raise ValueError("batch size must be positive")
        iterator = iter(self)
        while True:
            batch = list(islice(iterator, size))
            if not batch:
                return
            yield batch
