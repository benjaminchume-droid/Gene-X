"""Browser-backed consultation boundary."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol

class BrowserAgentBackend(Protocol):
    def ask(self, question: Any, **kwargs: Any) -> Any: ...

@dataclass
class BrowserAgent:
    name: str
    backend: BrowserAgentBackend

    def ask(self, question: Any, **kwargs: Any) -> Any:
        return self.backend.ask(question, **kwargs)

    def consult(self, request: Any) -> Any:
        question = getattr(request, "question", request)
        context = getattr(request, "context", None)
        return self.ask(question, context=context)
