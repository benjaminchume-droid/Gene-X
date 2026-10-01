"""World entities: stable identities with extensible attributes."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass(slots=True)
class Entity:
    kind: str
    name: str | None = None
    entity_id: str = field(default_factory=lambda: str(uuid4()))
    attributes: dict[str, Any] = field(default_factory=dict)

    def set(self, key: str, value: Any) -> None:
        self.attributes[key] = value
