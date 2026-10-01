"""General-purpose conceptual representation independent of language tokens."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass(frozen=True)
class Concept:
    name: str
    value: Any = None
    attributes: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass(frozen=True)
class Relation:
    source: str
    relation: str
    target: str
    confidence: float = 1.0
    attributes: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid4()))

@dataclass
class ConceptGraph:
    concepts: dict[str, Concept] = field(default_factory=dict)
    relations: dict[str, Relation] = field(default_factory=dict)

    def add(self, concept: Concept) -> Concept:
        self.concepts[concept.id] = concept
        return concept

    def relate(self, source: Concept | str, relation: str, target: Concept | str, *, confidence: float = 1.0, attributes: dict[str, Any] | None = None) -> Relation:
        s = source.id if isinstance(source, Concept) else source
        t = target.id if isinstance(target, Concept) else target
        if s not in self.concepts or t not in self.concepts:
            raise KeyError("both relation endpoints must exist in the graph")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        r = Relation(s, relation, t, confidence, attributes or {})
        self.relations[r.id] = r
        return r

    def related(self, concept: Concept | str, relation: str | None = None) -> list[Relation]:
        cid = concept.id if isinstance(concept, Concept) else concept
        return [r for r in self.relations.values() if r.source == cid and (relation is None or r.relation == relation)]
