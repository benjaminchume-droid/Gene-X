"""Gene-level trainable organism session."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from gene.learning.engine import ExperienceTrainer
from gene.learning.experience import Experience
from gene.learning.organism import LearningOrganism, OrganismStep
from gene.learning.signals import LearningSignal
from gene.memory.consolidation import Consolidator
from gene.memory.store import MemoryStore, MemoryRecord

@dataclass(frozen=True, slots=True)
class GeneTrainingReport:
    steps: int
    mean_score: float
    outcomes: tuple[OrganismStep, ...]

class GeneTrainingSession:
    """Trains Gene from supplied experience without embedding domain curriculum."""
    def __init__(
        self,
        organism: LearningOrganism,
        *,
        memory: MemoryStore | None = None,
        consolidator: Consolidator | None = None,
        teachers: Iterable[Callable[[Experience], Iterable[LearningSignal]]] = (),
    ) -> None:
        self.organism=organism
        self.memory=memory or MemoryStore()
        self.consolidator=consolidator or Consolidator()
        self.trainer=ExperienceTrainer(organism,teachers)

    def train(self, experiences: Iterable[Experience]) -> GeneTrainingReport:
        outcomes=[]
        for experience in experiences:
            step=self.trainer.step(experience)
            outcomes.append(step)
            self.memory.put(MemoryRecord(
                key=f"training:{self.organism.step_count}",
                value=experience,
                kind="training-experience",
                metadata={"score":step.score,"source":experience.source},
            ))
        scores=[step.score for step in outcomes]
        return GeneTrainingReport(len(outcomes),sum(scores)/len(scores) if scores else 0.0,tuple(outcomes))

    def replay(self, experiences: Iterable[tuple[Experience,Iterable[LearningSignal]]]) -> tuple[OrganismStep,...]:
        return self.organism.replay(experiences)

    def consolidate(self) -> int:
        records=tuple(self.memory.records(kind="training-experience"))
        retained=self.consolidator.consolidate(records)
        result=self.consolidator.commit(self.memory,retained)
        return result.retained
