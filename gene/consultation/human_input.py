"""Human-in-the-loop consultation boundary."""
from __future__ import annotations
from typing import Any, Callable

class HumanInput:
    def __init__(self, request: Callable[[str, Any], Any]) -> None:
        self.request = request

    def ask(self, question: str, context: Any = None) -> Any:
        if not question.strip():
            raise ValueError("question must not be empty")
        return self.request(question, context)
