"""Teacher interface. A teacher may be a model, human, test, document, tool, or environment."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class Teacher(ABC):
    @abstractmethod
    def teach(self, attempt: Any, context: Any = None) -> Any:
        raise NotImplementedError
