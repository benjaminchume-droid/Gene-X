"""External model boundary. Models are providers, not authorities."""
from __future__ import annotations
from typing import Any, Protocol

class ExternalModel(Protocol):
    def generate(self, prompt: Any, **kwargs: Any) -> Any: ...

class ModelConsultant:
    def __init__(self, model: ExternalModel) -> None:
        self.model = model

    def ask(self, prompt: Any, **kwargs: Any) -> Any:
        return self.model.generate(prompt, **kwargs)
