"""In-memory objective persistence boundary."""
from __future__ import annotations
from .objectives import Objective

class ObjectiveStore:
    def __init__(self) -> None:
        self._items: dict[str, Objective] = {}

    def save(self, objective: Objective) -> None:
        self._items[objective.objective_id] = objective

    def get(self, objective_id: str) -> Objective | None:
        return self._items.get(objective_id)

    def active(self) -> list[Objective]:
        return [x for x in self._items.values() if x.status.value == "active"]

    def all(self) -> list[Objective]:
        return list(self._items.values())
