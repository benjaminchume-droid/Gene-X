"""Benchmark runner with no embedded domain assumptions."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True, slots=True)
class BenchmarkCase:
    case_id: str
    input: Any
    expected: Any = None
    metadata: dict[str, Any] | None = None

@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    case_id: str
    score: float
    passed: bool
    output: Any

class BenchmarkRunner:
    def run(self, cases: Iterable[BenchmarkCase], system: Callable[[Any], Any], judge: Callable[[BenchmarkCase, Any], tuple[float, bool]]) -> tuple[BenchmarkResult, ...]:
        results = []
        for case in cases:
            output = system(case.input)
            score, passed = judge(case, output)
            results.append(BenchmarkResult(case.case_id, float(score), bool(passed), output))
        return tuple(results)
