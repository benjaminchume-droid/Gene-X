"""Typed relations between entities."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass(frozen=True, slots=True)
class Relation:
    subject: str
    predicate: str
    object: str
    relation_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)
