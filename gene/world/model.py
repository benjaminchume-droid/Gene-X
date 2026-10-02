"""Persistent world-state primitives independent of any particular domain."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Mapping
from uuid import uuid4

@dataclass(frozen=True)
class WorldEntity:
    entity_id: str = field(default_factory=lambda: uuid4().hex)
    attributes: Mapping[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class WorldRelation:
    source: str
    relation: str
    target: str
    confidence: float = 1.0

@dataclass
class WorldState:
    entities: dict[str, WorldEntity] = field(default_factory=dict)
    relations: list[WorldRelation] = field(default_factory=list)
    state: dict[str, Any] = field(default_factory=dict)
    revision: int = 0

    def upsert(self, entity: WorldEntity) -> None:
        self.entities[entity.entity_id] = entity
        self.revision += 1

    def relate(self, relation: WorldRelation) -> None:
        if relation not in self.relations:
            self.relations.append(relation)
            self.revision += 1

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value
        self.revision += 1

    def snapshot(self) -> dict[str, Any]:
        return {
            "revision": self.revision,
            "entities": {k: dict(v.attributes) for k, v in self.entities.items()},
            "relations": [r.__dict__ for r in self.relations],
            "state": dict(self.state),
        }
