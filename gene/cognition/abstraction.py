"""Reusable abstraction primitives over observed items."""
from __future__ import annotations
from collections import Counter
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")
K = TypeVar("K")

def group_by(items: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    groups: dict[K, list[T]] = {}
    for item in items:
        groups.setdefault(key(item), []).append(item)
    return groups

def frequencies(items: Iterable[T]) -> Counter[T]:
    return Counter(items)
