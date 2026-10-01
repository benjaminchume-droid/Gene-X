"""Interface for optional learned or deterministic capability providers."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class CapabilityProvider(ABC):
    name: str

    @abstractmethod
    def capabilities(self) -> set[str]:
        raise NotImplementedError

    @abstractmethod
    def invoke(self, capability: str, input: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
