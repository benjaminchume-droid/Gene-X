"""Typed relations between entities."""
from __future__ import annotations
from dataclasses import dataclass
from uuid import uuid4

@dataclass(frozen=True, slots=True)
class Relation:
    subject: str
    predicate: str
    object: str
    relation_id: str = uuid4().hex
    metadata: dict[str, object] | None = None
