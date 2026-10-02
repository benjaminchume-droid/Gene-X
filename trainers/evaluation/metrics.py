"""Composable evaluation metrics."""
from __future__ import annotations
from typing import Any, Callable

def exact_match(expected: Any, actual: Any) -> float:
    return 1.0 if expected == actual else 0.0

def threshold(predicate: Callable[[Any, Any], bool]) -> Callable[[Any, Any], float]:
    return lambda expected, actual: 1.0 if predicate(expected, actual) else 0.0

def mean(scores: list[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0
