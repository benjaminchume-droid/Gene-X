"""Computer-control boundary. Concrete UI/OS adapters are injected."""
from __future__ import annotations
from typing import Any, Protocol

class ComputerBackend(Protocol):
    def move(self, x: int, y: int) -> Any: ...
    def click(self, button: str = "left") -> Any: ...
    def type_text(self, text: str) -> Any: ...
    def key(self, key: str) -> Any: ...

class ComputerTool:
    def __init__(self, backend: ComputerBackend) -> None:
        self.backend = backend

    def move(self, x: int, y: int) -> Any:
        return self.backend.move(x, y)

    def click(self, button: str = "left") -> Any:
        return self.backend.click(button)

    def type_text(self, text: str) -> Any:
        return self.backend.type_text(text)

    def key(self, key: str) -> Any:
        return self.backend.key(key)
