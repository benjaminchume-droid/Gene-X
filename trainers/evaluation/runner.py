"""Evaluation runner for arbitrary callable systems."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True, slots=True)
class EvaluationResult:
    name: str
    passed: bool
    score: float
    details: dict[str, Any]

@dataclass(frozen=True, slots=True)
class EvaluationReport:
    results: tuple[EvaluationResult, ...]
    mean_score: float

class EvaluationRunner:
    def run(
        self,
        cases: Iterable[tuple[str, Any]],
        system: Callable[[Any], Any],
        judge: Callable[[Any, Any], tuple[bool, float, dict[str, Any]]],
    ) -> EvaluationReport:
        results = []
        for name, case in cases:
            output = system(case)
            passed, score, details = judge(case, output)
            results.append(EvaluationResult(name, passed, float(score), details))
        mean = sum(r.score for r in results) / len(results) if results else 0.0
        return EvaluationReport(tuple(results), mean)
