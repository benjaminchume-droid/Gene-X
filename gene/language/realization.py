"""Language realization from structured representations."""
from __future__ import annotations
from typing import Any, Callable

class Realizer:
    def __init__(self, render: Callable[[Any], str]) -> None:
        self.render = render

    def realize(self, representation: Any) -> str:
        return self.render(representation)
