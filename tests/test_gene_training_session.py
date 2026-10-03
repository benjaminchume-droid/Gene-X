from gene.system import GeneSystem
from gene.learning.experience import Experience
from gene.learning.signals import LearningSignal
from gene.learning.organism import LearningOutcome

class Learner:
    def learn(self, experience, signals):
        return LearningOutcome(kind="test", delta=1.0)

def teacher(experience):
    return (LearningSignal(kind="feedback", value=1.0, source="test"),)

def test_gene_training_session_trains_the_organism():
    gene=GeneSystem()
    gene.learner.add(Learner())
    report=gene.training_session((teacher,)).train((Experience("x","y",{"ok":True},"test"),))
    assert report.steps==1 and report.mean_score==1.0
