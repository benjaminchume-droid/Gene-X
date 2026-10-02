"""Training entry point for Gene's non-monolithic learning architecture."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from gene.learning.organism import LearningOrganism, OrganismStep
from gene.learning.experience import Experience
from gene.learning.signals import LearningSignal

@dataclass
class TrainingReport:
    steps: int
    mean_score: float
    learned: int
    rejected: int

class OrganismTrainer:
    def __init__(self, organism: LearningOrganism):
        self.organism = organism

    def fit(self, stream: Iterable[tuple[Experience, Iterable[LearningSignal]]]) -> TrainingReport:
        steps = list(self.organism.replay(stream))
        scores = [s.score for s in steps]
        learned = sum(len(o.learned) for s in steps for o in s.outcomes)
        rejected = sum(len(o.discarded) for s in steps for o in s.outcomes)
        return TrainingReport(len(steps), sum(scores)/len(scores) if scores else 0.0, learned, rejected)
