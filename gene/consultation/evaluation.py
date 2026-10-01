"""Evaluation of external consultation results before they enter durable knowledge."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class ConsultationEvaluation:
    accepted: bool
    confidence: float
    rationale: str = ""
    evidence: tuple[Any, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

class ConsultationEvaluator:
    def __init__(self, evaluator: Callable[[Any], ConsultationEvaluation]) -> None:
        self._evaluator = evaluator

    def evaluate(self, result: Any) -> ConsultationEvaluation:
        return self._evaluator(result)
