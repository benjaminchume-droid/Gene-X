from gene.learning.environment import EnvironmentStep
from gene.learning.training import Trainer
class Env:
 def reset(self,seed=None):return 0
 def step(self,action):return EnvironmentStep(action,reward=float(action),done=True)
 def evaluate(self,result):return float(result)
def test_training_episode():
 ep=Trainer(lambda state:1).run_episode(Env());assert ep.completed and ep.total_reward==1
