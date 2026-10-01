"""Search capability boundary using an injected provider."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol

class SearchBackend(Protocol):
    def search(self, query: str, **kwargs: Any) -> Any: ...

@dataclass
class SearchTool:
    backend: SearchBackend

    def search(self, query: str, **kwargs: Any) -> Any:
        if not query.strip():
            raise ValueError("query must not be empty")
        return self.backend.search(query, **kwargs)
