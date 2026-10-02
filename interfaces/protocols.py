"""Stable boundaries for external Gene integrations."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Protocol

@dataclass(frozen=True, slots=True)
class Request:
    operation: str
    payload: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class Response:
    success: bool
    payload: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

class Interface(Protocol):
    def handle(self, request: Request) -> Response: ...
