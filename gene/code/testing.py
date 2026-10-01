"""Test execution boundary for generated or modified code."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True)
class TestResult:
    passed: bool
    output: Any = None
    error: Any = None

class TestRunner:
    def __init__(self, run: Callable[[Any], TestResult]) -> None:
        self.run_test = run

    def run(self, target: Any) -> TestResult:
        return self.run_test(target)

    def run_many(self, targets: Iterable[Any]) -> tuple[TestResult, ...]:
        return tuple(self.run(target) for target in targets)

    @staticmethod
    def all_passed(results: Iterable[TestResult]) -> bool:
        return all(result.passed for result in results)
