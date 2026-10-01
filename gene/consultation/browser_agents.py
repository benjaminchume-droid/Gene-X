"""Browser-agent boundary for external research and interaction."""
from __future__ import annotations
from typing import Any, Protocol

class BrowserAgent(Protocol):
    def research(self, objective: str, **kwargs: Any) -> Any: ...

class BrowserConsultant:
    def __init__(self, agent: BrowserAgent) -> None:
        self.agent = agent

    def research(self, objective: str, **kwargs: Any) -> Any:
        if not objective.strip():
            raise ValueError("objective must not be empty")
        return self.agent.research(objective, **kwargs)
