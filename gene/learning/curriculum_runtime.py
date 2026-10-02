"""Adaptive curriculum selection driven by measured capability."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable

@dataclass(frozen=True, slots=True)
class LessonScore:
    lesson_id:str
    score:float

@dataclass(frozen=True, slots=True)
class CurriculumDecision:
    lesson_id:str
    reason:str

class AdaptiveCurriculum:
    def __init__(self,lessons:Iterable[Any],identify:Callable[[Any],str],measure:Callable[[Any],float])->None:
        self.lessons=tuple(lessons); self.identify=identify; self.measure=measure
    def select(self,*,completed:frozenset[str]=frozenset())->CurriculumDecision|None:
        candidates=[x for x in self.lessons if self.identify(x) not in completed]
        if not candidates:return None
        _,lesson=min((float(self.measure(x)),x) for x in candidates)
        return CurriculumDecision(self.identify(lesson),"lowest measured capability among unfinished lessons")
