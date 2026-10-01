"""Synthesis boundary for combining independently sourced results."""
from __future__ import annotations
from typing import Any, Callable, Iterable

class Synthesizer:
    def __init__(self, combine: Callable[[tuple[Any, ...]], Any]) -> None:
        self.combine = combine

    def synthesize(self, results: Iterable[Any]) -> Any:
        return self.combine(tuple(results))
