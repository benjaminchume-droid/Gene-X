"""Invention primitives based on composition and explicit hypotheses."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True)
class Hypothesis:
    proposal: Any
    basis: tuple[Any, ...]

def compose(components: Iterable[Any], synthesizer: Callable[[tuple[Any, ...]], Any]) -> Hypothesis:
    basis = tuple(components)
    return Hypothesis(synthesizer(basis), basis)
