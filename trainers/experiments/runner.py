"""Reproducible experiment execution boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True, slots=True)
class ExperimentResult:
    name: str
    value: Any

class ExperimentRunner:
    def run(self, experiments: Iterable[tuple[str, Callable[[], Any]]]) -> tuple[ExperimentResult, ...]:
        return tuple(ExperimentResult(name, fn()) for name, fn in experiments)
