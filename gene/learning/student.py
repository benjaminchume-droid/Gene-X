"""Student protocol for systems that improve from evaluated experience."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class Student(ABC):
    @abstractmethod
    def attempt(self, task: Any, context: Any = None) -> Any:
        raise NotImplementedError

    @abstractmethod
    def learn(self, experience: Any, feedback: Any) -> None:
        raise NotImplementedError
