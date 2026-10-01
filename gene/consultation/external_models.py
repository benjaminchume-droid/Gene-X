"""External model boundary with explicit source identity."""
from __future__ import annotations
from typing import Any, Protocol

class ExternalModelBackend(Protocol):
    def generate(self, prompt: Any, **kwargs: Any) -> Any: ...

class ExternalModel:
    def __init__(self, name: str, backend: ExternalModelBackend) -> None:
        self.name = name
        self.backend = backend

    def generate(self, prompt: Any, **kwargs: Any) -> Any:
        return self.backend.generate(prompt, **kwargs)
