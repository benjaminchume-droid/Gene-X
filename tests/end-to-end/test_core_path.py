from gene.objectives.manager import ObjectiveManager
from gene.runtime.cognitive import CognitiveRuntime
def test_objective_to_task_execution():
    runtime=CognitiveRuntime(objectives=ObjectiveManager())
    objective=runtime.add_objective("integration")
    task=runtime.add_task(objective,lambda:"ok")
    result=runtime.run_ready()
    assert result[0].result=="ok"
    assert task.status.value=="succeeded"
