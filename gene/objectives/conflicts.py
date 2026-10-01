"""Generic conflict detection for simultaneously active objectives."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

from .model import Objective


@dataclass(frozen=True, slots=True)
class Conflict:
    left_id: str
    right_id: str
    reason: str


ConflictRule = Callable[[Objective, Objective], str | None]


class ConflictDetector:
    """Runs injected conflict rules; it does not assume domain-specific meaning."""

    def __init__(self, rules: Iterable[ConflictRule] = ()) -> None:
        self._rules = list(rules)

    def add_rule(self, rule: ConflictRule) -> None:
        self._rules.append(rule)

    def detect(self, objectives: Iterable[Objective]) -> tuple[Conflict, ...]:
        active = [o for o in objectives if o.status.value == "active"]
        conflicts: list[Conflict] = []
        for index, left in enumerate(active):
            for right in active[index + 1 :]:
                for rule in self._rules:
                    reason = rule(left, right)
                    if reason:
                        conflicts.append(Conflict(left.objective_id, right.objective_id, reason))
        return tuple(conflicts)
