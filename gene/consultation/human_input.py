"""Explicit human consultation boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class HumanRequest:
    question: str
    context: Any = None
    urgency: str = "normal"

@dataclass(frozen=True)
class HumanResponse:
    answer: Any
    respondent: str | None = None
    metadata: dict[str, Any] | None = None

class HumanConsultation:
    def __init__(self, request: Callable[[HumanRequest], HumanResponse]) -> None:
        self.request = request

    def ask(self, question: str, *, context: Any = None, urgency: str = "normal") -> HumanResponse:
        return self.request(HumanRequest(question, context, urgency))
