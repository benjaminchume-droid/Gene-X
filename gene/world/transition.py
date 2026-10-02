"""Domain-neutral learned transition memory.

A transition is an observed before/action/after relationship. It stores
experience rather than embedding any domain-specific state machine.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Iterable

@dataclass(frozen=True, slots=True)
class Transition:
    before: Any
    action: Any
    after: Any

@dataclass
class TransitionModel:
    transitions: list[Transition] = field(default_factory=list)

    def observe(self, before: Any, action: Any, after: Any) -> Transition:
        transition = Transition(before, action, after)
        self.transitions.append(transition)
        return transition

    def candidates(self, before: Any = None, action: Any = None) -> tuple[Transition, ...]:
        return tuple(
            item for item in self.transitions
            if (before is None or item.before == before)
            and (action is None or item.action == action)
        )

    def predict(self, before: Any, action: Any) -> tuple[Any, ...]:
        return tuple(item.after for item in self.candidates(before, action))
