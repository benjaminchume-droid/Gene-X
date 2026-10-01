"""Browser-agent boundary for externally hosted interfaces."""
from __future__ import annotations
from typing import Any, Protocol

class BrowserAgentBackend(Protocol):
    def run(self, objective: str, **kwargs: Any) -> Any: ...

class BrowserAgent:
    def __init__(self, backend: BrowserAgentBackend) -> None:
        self.backend = backend

    def run(self, objective: str, **kwargs: Any) -> Any:
        if not objective.strip():
            raise ValueError("objective must not be empty")
        return self.backend.run(objective, **kwargs)
