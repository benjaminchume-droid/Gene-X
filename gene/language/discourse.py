"""Conversation/discourse state without tying it to a context-window implementation."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class DiscourseState:
    turns: list[Any] = field(default_factory=list)
    focus: Any = None

    def add(self, turn: Any) -> None:
        self.turns.append(turn)

    def set_focus(self, focus: Any) -> None:
        self.focus = focus
