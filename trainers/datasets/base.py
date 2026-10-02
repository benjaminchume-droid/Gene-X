"""Dataset protocols and deterministic iteration primitives."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable, Iterator, Protocol

@dataclass(frozen=True, slots=True)
class Sample:
    value: Any
    target: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

class Dataset(Protocol):
    def __iter__(self) -> Iterator[Sample]: ...
    def __len__(self) -> int: ...

class InMemoryDataset:
    def __init__(self, samples: Iterable[Sample]) -> None:
        self._samples = tuple(samples)
    def __iter__(self) -> Iterator[Sample]:
        return iter(self._samples)
    def __len__(self) -> int:
        return len(self._samples)
