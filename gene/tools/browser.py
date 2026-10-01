"""Minimal browser transport boundary.

The runtime depends on an injected browser implementation. This keeps browser
access real while avoiding a fake browser baked into Gene X.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol

class BrowserBackend(Protocol):
    def open(self, url: str) -> Any: ...
    def close(self) -> None: ...

@dataclass
class BrowserTool:
    backend: BrowserBackend

    def open(self, url: str) -> Any:
        if not url:
            raise ValueError("url must not be empty")
        return self.backend.open(url)

    def close(self) -> None:
        self.backend.close()
