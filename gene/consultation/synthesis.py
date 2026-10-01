"""Combine independently sourced consultation results while retaining provenance."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from .manager import ConsultationResponse

@dataclass(frozen=True)
class Synthesis:
    result: Any
    sources: tuple[str, ...]
    inputs: tuple[ConsultationResponse, ...]

class Synthesizer:
    def __init__(self, combine: Callable[[tuple[Any, ...]], Any]) -> None:
        self.combine = combine

    def synthesize(self, responses: Iterable[ConsultationResponse]) -> Synthesis:
        values = tuple(responses)
        return Synthesis(
            result=self.combine(tuple(r.answer for r in values)),
            sources=tuple(r.source for r in values),
            inputs=values,
        )
