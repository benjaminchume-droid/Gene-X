"""Static code-analysis boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class Diagnostic:
    severity: str
    message: str
    location: Any = None

class CodeAnalyzer:
    def __init__(self, analyze: Callable[[Any], list[Diagnostic]]) -> None:
        self.analyze = analyze

    def run(self, source: Any) -> list[Diagnostic]:
        return self.analyze(source)
