"""External model boundary with explicit source identity and capability metadata."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol

class ExternalModelBackend(Protocol):
    def generate(self, prompt: Any, **kwargs: Any) -> Any: ...

@dataclass
class ExternalModel:
    name: str
    backend: ExternalModelBackend
    metadata: dict[str, Any] = field(default_factory=dict)

    def generate(self, prompt: Any, **kwargs: Any) -> Any:
        return self.backend.generate(prompt, **kwargs)

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "metadata": dict(self.metadata)}
