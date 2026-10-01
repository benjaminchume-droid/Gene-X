"""Exact arithmetic primitives."""
from __future__ import annotations
from decimal import Decimal

def add(*values: int | float | Decimal):
    return sum(values, 0)

def subtract(left, right):
    return left - right

def multiply(*values):
    result = 1
    for value in values:
        result *= value
    return result

def divide(left, right):
    if right == 0:
        raise ZeroDivisionError("division by zero")
    return left / right
