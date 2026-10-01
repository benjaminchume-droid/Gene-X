"""Human-in-the-loop boundary for unresolved decisions and verification."""
from __future__ import annotations
from typing import Any, Callable

class HumanInput:
    def __init__(self, request: Callable[[Any], Any]) -> None:
        self.request = request

    def ask(self, question: Any) -> Any:
        return self.request(question)
