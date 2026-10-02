from gene.training_runtime import TrainingExample,TrainingRuntime
class Learner:
    def __init__(self): self.values=[]
    def learn(self,e): self.values.append(e.input); return 0.0
def test_training_runtime():
    l=Learner(); report=TrainingRuntime(l).run([TrainingExample(1),TrainingExample(2)])
    assert len(report.steps)==2 and l.values==[1,2]
