"""General-purpose world state graph."""
from __future__ import annotations
from dataclasses import dataclass, field
from .entities import Entity
from .relations import Relation

@dataclass(slots=True)
class World:
    entities: dict[str, Entity] = field(default_factory=dict)
    relations: dict[str, Relation] = field(default_factory=dict)

    def add_entity(self, entity: Entity) -> Entity:
        self.entities[entity.entity_id] = entity
        return entity

    def add_relation(self, relation: Relation) -> Relation:
        if relation.subject not in self.entities or relation.object not in self.entities:
            raise KeyError("relations require existing subject and object entities")
        self.relations[relation.relation_id] = relation
        return relation

    def related(self, entity_id: str, predicate: str | None = None) -> list[Relation]:
        return [r for r in self.relations.values()
                if (r.subject == entity_id or r.object == entity_id)
                and (predicate is None or r.predicate == predicate)]
