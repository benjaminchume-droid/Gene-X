"""Language-facing structures that bridge linguistic input and Gene's substrate."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass(frozen=True)
class Proposition:
    predicate: str
    arguments: dict[str, Any] = field(default_factory=dict)
    modality: str | None = None
    confidence: float = 1.0
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass(frozen=True)
class Intent:
    kind: str
    target: Any = None
    parameters: dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0

@dataclass
class LanguageRepresentation:
    propositions: list[Proposition] = field(default_factory=list)
    intent: Intent | None = None
    references: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
