"""Durable bridge between objectives, task execution, recovery, cognition and learning."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable
from gene.objectives.manager import ObjectiveManager
from gene.objectives.model import Objective, ObjectiveChange, ObjectiveStatus
from gene.tasks.task import Task, TaskStatus
from gene.tasks.graph import TaskGraph
from gene.learning.experience import Experience
from .events import Event, EventBus
from .recovery import RecoveryPolicy
from .learning_loop import LearningLoop

@dataclass(frozen=True, slots=True)
class ExecutionRecord:
    task_id: str
    status: TaskStatus
    result: Any = None
    error: str | None = None
    learning_score: float | None = None

@dataclass
class CognitiveRuntime:
    """Runs mutable plans while keeping objectives durable and learning from execution."""
    objectives: ObjectiveManager = field(default_factory=ObjectiveManager)
    graph: TaskGraph = field(default_factory=TaskGraph)
    events: EventBus = field(default_factory=EventBus)
    recovery: RecoveryPolicy = field(default_factory=RecoveryPolicy)
    learning: LearningLoop | None = None
    _operations: dict[str, Callable[[], Any]] = field(default_factory=dict)

    def add_objective(self, description: str, **metadata: Any) -> Objective:
        objective = self.objectives.create(description, **metadata)
        self.events.publish(Event("objective.created", {"objective_id": objective.objective_id}))
        return objective

    def add_task(self, objective: Objective | str, operation: Callable[[], Any], *, dependencies: set[str] = (), metadata: dict[str, Any] | None = None) -> Task:
        objective_id = objective if isinstance(objective, str) else objective.objective_id
        self.objectives.get(objective_id)
        task = Task(objective=objective_id, dependencies=set(dependencies), metadata=metadata or {})
        self.graph.add(task)
        self._operations[task.task_id] = operation
        self.events.publish(Event("task.created", {"task_id": task.task_id, "objective_id": objective_id}))
        return task

    def attach_learning(self, learning: LearningLoop) -> None:
        self.learning = learning

    def amend_objective(self, objective_id: str, change: ObjectiveChange) -> Objective:
        objective = self.objectives.amend(objective_id, change)
        self.events.publish(Event("objective.amended", {"objective_id": objective_id, "version": objective.version}))
        return objective

    def ready(self) -> tuple[Task, ...]:
        return tuple(self.graph.ready())

    def run_ready(self, *, limit: int | None = None, objective_ids: Iterable[str] | None = None) -> tuple[ExecutionRecord, ...]:
        allowed = None if objective_ids is None else set(objective_ids)
        ready = self.ready()
        if allowed is not None:
            ready = tuple(task for task in ready if task.objective in allowed)
        tasks = ready[:limit] if limit is not None else ready
        records: list[ExecutionRecord] = []
        for task in tasks:
            task.status = TaskStatus.RUNNING
            error: Exception | None = None
            result: Any = None
            try:
                result = self._operations[task.task_id]()
                task.result = result
                task.status = TaskStatus.SUCCEEDED
                task.error = None
                self.events.publish(Event("task.succeeded", {"task_id": task.task_id}))
            except Exception as exc:
                error = exc
                task.status = TaskStatus.FAILED
                task.error = repr(exc)
                try:
                    recovered = self.recovery.recover(exc)
                    task.result = recovered
                    task.status = TaskStatus.SUCCEEDED
                    result = recovered
                    self.events.publish(Event("task.recovered", {"task_id": task.task_id}))
                except Exception as recovery_error:
                    result = None
                    error = recovery_error
                    self.events.publish(Event("task.failed", {"task_id": task.task_id}))
            score = None
            if self.learning is not None:
                experience = Experience(
                    input={"task_id": task.task_id, "objective": task.objective, "metadata": dict(task.metadata)},
                    output=result,
                    outcome={"status": task.status.value, "error": repr(error) if error else None},
                    source="runtime",
                    metadata={"task_id": task.task_id, "objective_id": task.objective},
                )
                learned = self.learning.observe(experience)
                score = learned.score
                self.events.publish(Event("task.learned", {"task_id": task.task_id, "score": score}))
            records.append(ExecutionRecord(task.task_id, task.status, result, repr(error) if error else None, score))
        self._complete_objectives()
        return tuple(records)

    def _complete_objectives(self) -> None:
        for objective in self.objectives.active():
            tasks = [t for t in self.graph.tasks.values() if t.objective == objective.objective_id]
            if tasks and all(t.status == TaskStatus.SUCCEEDED for t in tasks):
                objective.status = ObjectiveStatus.COMPLETED
                self.events.publish(Event("objective.completed", {"objective_id": objective.objective_id}))
