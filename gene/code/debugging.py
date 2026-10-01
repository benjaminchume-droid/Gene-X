"""Failure diagnosis primitives that preserve observed evidence."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable

@dataclass(frozen=True)
class Failure:
    message: str
    source: str | None = None
    location: Any = None
    evidence: tuple[Any, ...] = ()

@dataclass(frozen=True)
class Diagnosis:
    failure: Failure
    hypotheses: tuple[str, ...]
    next_checks: tuple[str, ...]

class Debugger:
    def diagnose(self, failure: Failure, hypotheses: Iterable[str], next_checks: Iterable[str] = ()) -> Diagnosis:
        return Diagnosis(failure, tuple(hypotheses), tuple(next_checks))

    def narrow(self, diagnosis: Diagnosis, *, keep: Iterable[int]) -> Diagnosis:
        indexes = set(keep)
        hypotheses = tuple(value for i, value in enumerate(diagnosis.hypotheses) if i in indexes)
        return Diagnosis(diagnosis.failure, hypotheses, diagnosis.next_checks)
