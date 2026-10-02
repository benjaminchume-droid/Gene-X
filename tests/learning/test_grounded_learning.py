from gene.brain.representation import StructuredExample, TrainableRepresentation
from gene.brain.grounding import GroundedRepresentationTrainer, GroundedSample
from gene.learning.organism import LearningOrganism
from gene.learning.engine import ExperienceTrainer
from gene.learning.experience import Experience
from gene.learning.signals import LearningSignal, SignalKind
from gene.world.transition import TransitionModel

def test_grounded_representation_training():
    rep=TrainableRepresentation(representation_size=16, embedding_size=8, seed=1)
    ex=StructuredExample(concepts=("a",),state=(("s",1),))
    target=tuple(0.1 for _ in range(16))
    report=GroundedRepresentationTrainer(rep).fit_targets([GroundedSample(ex,target)],epochs=2)
    assert report.steps==2

def test_learning_organism_uses_teacher_signal():
    class Component:
        def learn(self,experience,signals):
            from gene.learning.signals import LearningOutcome
            return LearningOutcome(bool(signals), sum(s.value or 0 for s in signals))
    organism=LearningOrganism([Component()])
    trainer=ExperienceTrainer(organism,[lambda e:(LearningSignal(SignalKind.REWARD,1.0,source="test"),)])
    result=trainer.step(Experience("i","o","ok","test"))
    assert result.score==1.0

def test_transition_model_records_experience():
    model=TransitionModel()
    item=model.observe("before","action","after")
    assert item in model.transitions
