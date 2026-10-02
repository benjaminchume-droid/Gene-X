"""Production coordination surface for Gene X.

This layer connects the existing objective, runtime, memory, learning, and
journal primitives. It contains no domain knowledge or fixed task paths.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from gene.memory.store import MemoryRecord, MemoryStore
from gene.objectives.model import Objective
from .arbiter import ObjectiveArbiter, ResourceBudget
from .cognitive import CognitiveRuntime, ExecutionRecord
from .journal import RuntimeJournal

@dataclass(frozen=True, slots=True)
class OrganismObservation:
    records: tuple[ExecutionRecord, ...]
    memories_written: int
    journal_sequence: int

@dataclass
class GeneOrganism:
    runtime: CognitiveRuntime = field(default_factory=CognitiveRuntime)
    memory: MemoryStore = field(default_factory=MemoryStore)
    journal: RuntimeJournal = field(default_factory=RuntimeJournal)
    arbiter: ObjectiveArbiter = field(default_factory=ObjectiveArbiter)

    def create_objective(self, description: str, **metadata: Any) -> Objective:
        objective = self.runtime.add_objective(description, **metadata)
        self.journal.append("objective.created", {"objective_id": objective.objective_id, "version": objective.version})
        return objective

    def add_task(self, objective: Objective | str, operation: Callable[[], Any], *, dependencies: set[str] = (), metadata: dict[str, Any] | None = None):
        task = self.runtime.add_task(objective, operation, dependencies=dependencies, metadata=metadata)
        self.journal.append("task.created", {"task_id": task.task_id, "objective_id": task.objective})
        return task

    def observe(self, *, limit: int | None = None) -> OrganismObservation:
        concurrency = limit if limit is not None else 1
        arbitration = self.arbiter.select(
            self.runtime.objectives.active(),
            conflicts=self.runtime.objectives.conflicts(),
            budget=ResourceBudget(concurrent=concurrency),
        )
        self.journal.append("objectives.arbitrated", {"selected": arbitration.selected, "deferred": arbitration.deferred})
        records = self.runtime.run_ready(
            limit=limit,
            objective_ids=arbitration.selected,
        )
        written = 0
        for record in records:
            self.journal.append("task.execution", {
                "task_id": record.task_id,
                "status": record.status.value,
                "learning_score": record.learning_score,
            })
            key = f"execution:{record.task_id}:{len(self.journal.entries())}"
            self.memory.put(MemoryRecord(
                key=key,
                value={"task_id": record.task_id, "status": record.status.value, "result": record.result, "error": record.error},
                kind="episode",
                metadata={"source": "runtime", "sequence": self.journal.entries()[-1].sequence},
            ))
            written += 1
        return OrganismObservation(records, written, len(self.journal.entries()))

    def remember(self, key: str, value: Any, *, kind: str = "general", metadata: dict[str, Any] | None = None) -> None:
        self.memory.put(MemoryRecord(key=key, value=value, kind=kind, metadata=metadata or {}))
        self.journal.append("memory.written", {"key": key, "kind": kind})

    def snapshot(self) -> dict[str, Any]:
        return {
            "journal": [{"sequence": e.sequence, "event": e.event, "payload": e.payload} for e in self.journal.entries()],
            "memory": [{"key": r.key, "value": r.value, "kind": r.kind, "metadata": r.metadata} for r in self.memory.records()],
            "objectives": [
                {"objective_id": o.objective_id, "description": o.description, "status": o.status.value, "version": o.version, "metadata": dict(o.metadata)}
                for o in self.runtime.objectives.objectives.values()
            ],
        }
