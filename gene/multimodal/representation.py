"""Modality-independent representation primitives.

A representation identifies structured information without prescribing how it is
rendered or which model produced it.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

@dataclass(slots=True)
class Representation:
    kind: str
    data: Any
    attributes: dict[str, Any] = field(default_factory=dict)
    representation_id: str = field(default_factory=lambda: str(uuid4()))

    def attribute(self, name: str, default: Any = None) -> Any:
        return self.attributes.get(name, default)
