"""Language generation boundary separate from parsing and realization."""
from __future__ import annotations
from typing import Any, Protocol

class GeneratorBackend(Protocol):
    def generate(self, representation: Any, **kwargs: Any) -> str: ...

class LanguageGenerator:
    def __init__(self, backend: GeneratorBackend) -> None:
        self.backend = backend

    def generate(self, representation: Any, **kwargs: Any) -> str:
        return self.backend.generate(representation, **kwargs)
