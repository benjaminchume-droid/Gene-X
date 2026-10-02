"""Generic capability evaluation runner."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable

@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    input: Any
    expected: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class BenchmarkResult:
    case_id: str
    passed: bool
    score: float
    output: Any = None
    error: str | None = None

class BenchmarkRunner:
    def __init__(self, evaluator: Callable[[Any], Any]):
        self.evaluator = evaluator

    def run(self, cases: Iterable[BenchmarkCase]) -> tuple[BenchmarkResult, ...]:
        results = []
        for case in cases:
            try:
                output = self.evaluator(case.input)
                passed = case.expected is None or output == case.expected
                results.append(BenchmarkResult(case.case_id, passed, 1.0 if passed else 0.0, output))
            except Exception as exc:
                results.append(BenchmarkResult(case.case_id, False, 0.0, error=repr(exc)))
        return tuple(results)
