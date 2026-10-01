"""Generalization boundary for deriving reusable behavior from examples."""
from __future__ import annotations
from typing import Any, Callable, Iterable

class Generalizer:
    def __init__(self, derive: Callable[[tuple[Any, ...]], Any]) -> None:
        self.derive = derive

    def generalize(self, experiences: Iterable[Any]) -> Any:
        return self.derive(tuple(experiences))
