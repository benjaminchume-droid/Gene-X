"""Language parsing boundary. Concrete parsers are injected."""
from __future__ import annotations
from typing import Any, Protocol

class ParserBackend(Protocol):
    def parse(self, text: str) -> Any: ...

class Parser:
    def __init__(self, backend: ParserBackend) -> None:
        self.backend = backend

    def parse(self, text: str) -> Any:
        if not text.strip():
            raise ValueError("text must not be empty")
        return self.backend.parse(text)
