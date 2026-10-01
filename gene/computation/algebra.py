"""Exact algebraic primitives."""
from __future__ import annotations
from fractions import Fraction
from dataclasses import dataclass

@dataclass(frozen=True)
class LinearTerm:
    coefficient: Fraction
    variable: str

def rational(value: int | float | str) -> Fraction:
    return Fraction(value)

def solve_linear(a: int | float | Fraction, b: int | float | Fraction) -> Fraction:
    if a == 0:
        raise ValueError("coefficient cannot be zero")
    return Fraction(-b) / Fraction(a)

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)
