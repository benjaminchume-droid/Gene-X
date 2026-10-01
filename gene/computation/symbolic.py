"""Symbolic expression primitives independent of a particular solver."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Symbol:
    name: str

@dataclass(frozen=True)
class Expression:
    operator: str
    operands: tuple[Any, ...]

    def __iter__(self):
        return iter(self.operands)
