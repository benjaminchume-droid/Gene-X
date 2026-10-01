"""Orchestrate external consultation without treating answers as truth."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True)
class ConsultationRequest:
    question: Any
    context: Any = None
    constraints: dict[str, Any] | None = None

@dataclass(frozen=True)
class ConsultationResult:
    source: str
    answer: Any
    metadata: dict[str, Any] | None = None

class ConsultationManager:
    def __init__(self) -> None:
        self._sources: dict[str, Callable[[ConsultationRequest], Any]] = {}

    def register(self, name: str, source: Callable[[ConsultationRequest], Any]) -> None:
        if name in self._sources:
            raise ValueError(f"source already registered: {name}")
        self._sources[name] = source

    def consult(self, request: ConsultationRequest, source: str) -> ConsultationResult:
        if source not in self._sources:
            raise LookupError(f"unknown consultation source: {source}")
        return ConsultationResult(source, self._sources[source](request))
