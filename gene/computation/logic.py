"""Small exact logical primitives."""
from __future__ import annotations
from collections.abc import Iterable

def conjunction(values: Iterable[bool]) -> bool:
    return all(values)

def disjunction(values: Iterable[bool]) -> bool:
    return any(values)

def implication(condition: bool, consequence: bool) -> bool:
    return (not condition) or consequence
