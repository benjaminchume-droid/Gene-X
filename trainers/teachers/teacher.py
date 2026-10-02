"""Teacher protocol; a teacher may be human, model, tool, test suite, or environment."""
from __future__ import annotations
from typing import Any, Protocol

class Teacher(Protocol):
    def __call__(self, input: Any, output: Any) -> Any: ...
