"""General-purpose world representation primitives.

Nothing in this module assumes particular real-world entities, labels, or
domains. Concrete knowledge is learned or supplied as data.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Entity:
    entity_type: str
    entity_id: str = field(default_factory=lambda: str(uuid4()))
    properties: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True, slots=True)
class Property:
    subject: str
    name: str
    value: Any
    confidence: float = 1.0
    source: str | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class Event:
    event_type: str
    participants: tuple[str, ...] = ()
    properties: dict[str, Any] = field(default_factory=dict)
    observed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True, slots=True)
class CausalLink:
    cause: str
    effect: str
    strength: float = 1.0
    evidence: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not 0.0 <= self.strength <= 1.0:
            raise ValueError("strength must be between 0 and 1")


@dataclass
class WorldModel:
    """Domain-neutral collection of entities, properties, events and causes."""

    entities: dict[str, Entity] = field(default_factory=dict)
    properties: list[Property] = field(default_factory=list)
    events: dict[str, Event] = field(default_factory=dict)
    causes: list[CausalLink] = field(default_factory=list)

    def add_entity(self, entity: Entity) -> Entity:
        self.entities[entity.entity_id] = entity
        return entity

    def add_property(self, prop: Property) -> Property:
        if prop.subject not in self.entities:
            raise KeyError("property subject is unknown")
        self.properties.append(prop)
        return prop

    def add_event(self, event: Event) -> Event:
        self.events[event.event_id] = event
        return event

    def add_cause(self, link: CausalLink) -> CausalLink:
        self.causes.append(link)
        return link

    def properties_of(self, entity_id: str) -> list[Property]:
        return [p for p in self.properties if p.subject == entity_id]
