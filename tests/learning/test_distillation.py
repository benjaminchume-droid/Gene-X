from trainers.distillation import DistillationLoop
class S:
    def __init__(self): self.updated=False
    def attempt(self,x): return x
    def update(self,*args): self.updated=True
def test_distillation():
    s=S(); DistillationLoop(lambda x:x,s,lambda a,b:a==b).run([1]); assert s.updated
