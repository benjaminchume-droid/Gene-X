"""Core Gene X runtime.

The runtime coordinates state and work. Intelligence is supplied by composable
cognition, memory, tools, and specialist components rather than embedded here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .events import Event, EventBus
from .state import RuntimeState

@dataclass(slots=True)
class Runtime:
    state: RuntimeState = field(default_factory=RuntimeState)
    events: EventBus = field(default_factory=EventBus)
    running: bool = False
    _steps: list[Callable[[RuntimeState], None]] = field(default_factory=list)

    def add_step(self, step: Callable[[RuntimeState], None]) -> None:
        self._steps.append(step)

    def start(self) -> None:
        self.running = True
        self.events.publish(Event("runtime.started", source="runtime"))

    def stop(self) -> None:
        self.running = False
        self.events.publish(Event("runtime.stopped", source="runtime"))

    def step(self) -> None:
        if not self.running:
            raise RuntimeError("runtime is not running")
        for operation in tuple(self._steps):
            operation(self.state)
        self.events.publish(Event("runtime.stepped",
                                  {"version": self.state.version},
                                  source="runtime"))
