"""Small composable reasoning primitives."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True)
class Inference:
    conclusion: Any
    premises: tuple[Any, ...]
    rule: str

def apply_rule(rule: Callable[..., Any], premises: Iterable[Any], name: str = "anonymous") -> Inference:
    values = tuple(premises)
    return Inference(rule(*values), values, name)
