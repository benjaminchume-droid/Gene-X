"""Objective arbitration primitives.

Scheduling policy is driven by objective metadata and dependency/conflict state.
No domain-specific priority table is embedded here.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from gene.objectives.model import Objective, ObjectiveStatus

@dataclass(frozen=True, slots=True)
class ResourceBudget:
    units: float = float("inf")
    concurrent: int = 1

@dataclass(frozen=True, slots=True)
class Arbitration:
    selected: tuple[str, ...]
    deferred: tuple[str, ...]
    reasons: dict[str, str]

class ObjectiveArbiter:
    def select(
        self,
        objectives: Iterable[Objective],
        *,
        conflicts: Iterable[object] = (),
        budget: ResourceBudget = ResourceBudget(),
    ) -> Arbitration:
        active = [o for o in objectives if o.status == ObjectiveStatus.ACTIVE]
        conflict_ids: set[str] = set()
        for conflict in conflicts:
            for name in ("left_id", "right_id", "objective_id"):
                value = getattr(conflict, name, None)
                if isinstance(value, str):
                    conflict_ids.add(value)
        def key(o: Objective) -> tuple[float, int, str]:
            raw = o.metadata.get("priority", 0)
            try:
                priority = float(raw)
            except (TypeError, ValueError):
                priority = 0.0
            return (-priority, len(o.dependencies), o.objective_id)
        active.sort(key=key)
        selected: list[str] = []
        deferred: list[str] = []
        reasons: dict[str, str] = {}
        for objective in active:
            if len(selected) >= max(0, budget.concurrent):
                deferred.append(objective.objective_id); reasons[objective.objective_id] = "concurrency_budget"
                continue
            if objective.objective_id in conflict_ids:
                deferred.append(objective.objective_id); reasons[objective.objective_id] = "objective_conflict"
                continue
            selected.append(objective.objective_id)
        return Arbitration(tuple(selected), tuple(deferred), reasons)
