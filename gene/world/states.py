"""Explicit state and state transitions."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True, slots=True)
class State:
    name: str
    values: dict[str, Any] = field(default_factory=dict)
@dataclass(frozen=True, slots=True)
class StateTransition:
    source: State
    target: State
    cause: str
    conditions: tuple[str, ...] = ()
