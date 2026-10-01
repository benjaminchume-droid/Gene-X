"""Modality-independent structured representations."""
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4
@dataclass(slots=True)
class Representation:
    kind: str
    data: Any
    attributes: dict[str, Any] = field(default_factory=dict)
    representation_id: str = field(default_factory=lambda: str(uuid4()))
    def attribute(self, name, default=None): return self.attributes.get(name, default)
