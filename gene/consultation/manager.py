"""Orchestrate independent consultation sources without treating answers as truth."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass(frozen=True)
class ConsultationRequest:
    question: Any
    context: Any = None
    constraints: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class ConsultationResult:
    source: str
    answer: Any
    metadata: dict[str, Any] = field(default_factory=dict)

class ConsultationManager:
    def __init__(self) -> None:
        self._sources: dict[str, Callable[[ConsultationRequest], Any]] = {}

    def register(self, name: str, source: Callable[[ConsultationRequest], Any]) -> None:
        if not name:
            raise ValueError("source name cannot be empty")
        if name in self._sources:
            raise ValueError(f"source already registered: {name}")
        self._sources[name] = source

    def sources(self) -> tuple[str, ...]:
        return tuple(self._sources)

    def consult(self, request: ConsultationRequest, source: str) -> ConsultationResult:
        try:
            provider = self._sources[source]
        except KeyError as exc:
            raise LookupError(f"unknown consultation source: {source}") from exc
        return ConsultationResult(source, provider(request))

    def consult_many(self, request: ConsultationRequest, sources: list[str] | None = None) -> tuple[ConsultationResult, ...]:
        selected = self.sources() if sources is None else tuple(sources)
        return tuple(self.consult(request, source) for source in selected)
