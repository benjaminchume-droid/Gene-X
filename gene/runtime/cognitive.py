"""Durable bridge between objectives, task execution, recovery and cognition."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable
from gene.objectives.manager import ObjectiveManager
from gene.objectives.model import Objective, ObjectiveChange, ObjectiveStatus
from gene.tasks.task import Task, TaskStatus
from gene.tasks.graph import TaskGraph
from .events import Event, EventBus
from .recovery import RecoveryPolicy

@dataclass(frozen=True, slots=True)
class ExecutionRecord:
    task_id: str
    status: TaskStatus
    result: Any = None
    error: str | None = None

@dataclass
class CognitiveRuntime:
    """Runs mutable plans while keeping objectives durable and independent."""
    objectives: ObjectiveManager = field(default_factory=ObjectiveManager)
    graph: TaskGraph = field(default_factory=TaskGraph)
    events: EventBus = field(default_factory=EventBus)
    recovery: RecoveryPolicy = field(default_factory=RecoveryPolicy)
    _operations: dict[str, Callable[[], Any]] = field(default_factory=dict)

    def add_objective(self, description: str, **metadata: Any) -> Objective:
        objective = self.objectives.create(description, **metadata)
        self.events.publish(Event("objective.created", {"objective_id": objective.objective_id}))
        return objective

    def add_task(self, objective: Objective | str, operation: Callable[[], Any], *,
                 dependencies: set[str] = (), metadata: dict[str, Any] | None = None) -> Task:
        objective_id = objective if isinstance(objective, str) else objective.objective_id
        self.objectives.get(objective_id)
        task = Task(objective=objective_id, dependencies=set(dependencies), metadata=metadata or {})
        self.graph.add(task); self._operations[task.task_id] = operation
        self.events.publish(Event("task.created", {"task_id": task.task_id, "objective_id": objective_id}))
        return task

    def amend_objective(self, objective_id: str, change: ObjectiveChange) -> Objective:
        objective=self.objectives.amend(objective_id, change)
        self.events.publish(Event("objective.amended", {"objective_id": objective_id, "version": objective.version}))
        return objective

    def ready(self) -> tuple[Task,...]:
        return tuple(self.graph.ready())

    def run_ready(self, *, limit: int | None = None) -> tuple[ExecutionRecord,...]:
        records=[]; tasks=self.ready()[:limit] if limit is not None else self.ready()
        for task in tasks:
            task.status=TaskStatus.RUNNING
            try:
                result=self._operations[task.task_id]()
                task.result=result; task.status=TaskStatus.SUCCEEDED; task.error=None
                record=ExecutionRecord(task.task_id,task.status,result)
                self.events.publish(Event("task.succeeded", {"task_id":task.task_id}))
            except Exception as error:
                task.status=TaskStatus.FAILED; task.error=repr(error)
                try:
                    recovered=self.recovery.recover(error)
                    task.result=recovered; task.status=TaskStatus.SUCCEEDED
                    record=ExecutionRecord(task.task_id,task.status,recovered)
                    self.events.publish(Event("task.recovered", {"task_id":task.task_id}))
                except Exception as recovery_error:
                    record=ExecutionRecord(task.task_id,task.status,error=repr(recovery_error))
                    self.events.publish(Event("task.failed", {"task_id":task.task_id}))
            records.append(record)
        self._complete_objectives()
        return tuple(records)

    def _complete_objectives(self) -> None:
        for objective in self.objectives.active():
            tasks=[t for t in self.graph.tasks.values() if t.objective==objective.objective_id]
            if tasks and all(t.status==TaskStatus.SUCCEEDED for t in tasks):
                objective.status=ObjectiveStatus.COMPLETED
                self.events.publish(Event("objective.completed", {"objective_id":objective.objective_id}))
