"""Static code-analysis primitives."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True)
class Diagnostic:
    severity: str
    message: str
    location: Any = None
    code: str | None = None

    def __post_init__(self) -> None:
        if self.severity not in {"info", "warning", "error"}:
            raise ValueError("severity must be info, warning, or error")

class CodeAnalyzer:
    def __init__(self, analyze: Callable[[Any], Iterable[Diagnostic]]) -> None:
        self.analyze = analyze

    def run(self, source: Any) -> tuple[Diagnostic, ...]:
        return tuple(self.analyze(source))

    @staticmethod
    def has_errors(diagnostics: Iterable[Diagnostic]) -> bool:
        return any(item.severity == "error" for item in diagnostics)

    @staticmethod
    def by_severity(diagnostics: Iterable[Diagnostic]) -> dict[str, tuple[Diagnostic, ...]]:
        grouped = {"info": [], "warning": [], "error": []}
        for diagnostic in diagnostics:
            grouped[diagnostic.severity].append(diagnostic)
        return {key: tuple(value) for key, value in grouped.items()}
