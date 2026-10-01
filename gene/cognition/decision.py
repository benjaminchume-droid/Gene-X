"""Decision primitive that keeps selection criteria explicit."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypeVar

T = TypeVar("T")

@dataclass(frozen=True)
class Decision(Generic[T]):
    option: T
    value: float

def choose(options: Iterable[T], score: Callable[[T], float]) -> Decision[T]:
    values = list(options)
    if not values:
        raise ValueError("cannot choose from empty options")
    option = max(values, key=score)
    return Decision(option, float(score(option)))
