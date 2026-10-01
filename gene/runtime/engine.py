"""Core runtime orchestration for persistent, incremental work."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any
from .state import RuntimeState
from .events import EventBus, Event

@dataclass
class Runtime:
    state: RuntimeState = field(default_factory=RuntimeState)
    events: EventBus = field(default_factory=EventBus)
    running: bool = False
    steps: int = 0

    def add_step(self, operation: Callable[[], Any]) -> Any:
        if not self.running:
            raise RuntimeError("runtime is not running")
        self.steps += 1
        result = operation()
        self.events.publish(Event(kind="step.completed", payload={"step": self.steps}))
        return result

    def start(self) -> None:
        self.running = True
        self.events.publish(Event(kind="runtime.started"))

    def stop(self) -> None:
        self.running = False
        self.events.publish(Event(kind="runtime.stopped"))

    def pause(self) -> None:
        self.running = False
        self.events.publish(Event(kind="runtime.paused"))

    def resume(self) -> None:
        self.running = True
        self.events.publish(Event(kind="runtime.resumed"))

    def run_until(self, predicate: Callable[[RuntimeState], bool], operation: Callable[[], Any]) -> None:
        if not self.running:
            raise RuntimeError("runtime is not running")
        while not predicate(self.state):
            self.add_step(operation)
