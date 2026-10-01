"""Evaluation boundary for tests, teachers, humans, and real-world outcomes."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Evaluation:
    passed: bool
    score: float
    feedback: Any = None

class Evaluator:
    def __init__(self, evaluate: Callable[[Any, Any], Evaluation]) -> None:
        self._evaluate = evaluate

    def evaluate(self, expected: Any, actual: Any) -> Evaluation:
        result = self._evaluate(expected, actual)
        if not 0.0 <= result.score <= 1.0:
            raise ValueError("evaluation score must be between 0 and 1")
        return result
