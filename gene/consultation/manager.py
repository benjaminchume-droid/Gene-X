"""Coordinate external information requests without treating responses as truth."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from uuid import uuid4

@dataclass(frozen=True)
class ConsultationRequest:
    question: Any
    request_id: str = field(default_factory=lambda: uuid4().hex)
    context: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ConsultationResponse:
    request_id: str
    source: str
    answer: Any
    metadata: dict[str, Any] = field(default_factory=dict)

class ConsultationManager:
    def __init__(self) -> None:
        self._providers: dict[str, Callable[[ConsultationRequest], Any]] = {}

    def register(self, name: str, provider: Callable[[ConsultationRequest], Any]) -> None:
        if name in self._providers:
            raise ValueError(f"consultation provider already registered: {name}")
        self._providers[name] = provider

    def ask(self, request: ConsultationRequest, provider: str) -> ConsultationResponse:
        if provider not in self._providers:
            raise LookupError(f"unknown consultation provider: {provider}")
        answer = self._providers[provider](request)
        return ConsultationResponse(request.request_id, provider, answer)
