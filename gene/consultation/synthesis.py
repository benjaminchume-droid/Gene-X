"""Synthesis primitives for combining independently sourced results."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True)
class SynthesisInput:
    source: str
    answer: Any
    metadata: dict[str, Any]

@dataclass(frozen=True)
class SynthesisResult:
    value: Any
    sources: tuple[str, ...]

class Synthesizer:
    def __init__(self, combine: Callable[[tuple[SynthesisInput, ...]], Any]) -> None:
        self.combine = combine

    def synthesize(self, results: Iterable[Any]) -> SynthesisResult:
        normalized = tuple(
            item if isinstance(item, SynthesisInput)
            else SynthesisInput(getattr(item, "source", "unknown"), getattr(item, "answer", item), getattr(item, "metadata", {}))
            for item in results
        )
        return SynthesisResult(self.combine(normalized), tuple(item.source for item in normalized))
