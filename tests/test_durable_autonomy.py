from gene.runtime.cognitive import CognitiveRuntime
from gene.runtime.autonomous_durable import DurableAutonomousDriver
from gene.runtime.persistence import RuntimePersistence

def test_durable_autonomy_checkpoint_survives_cycle(tmp_path):
    runtime=CognitiveRuntime()
    objective=runtime.add_objective("durable")
    runtime.add_task(objective,lambda: 4)
    path=tmp_path/"state.json"
    run=DurableAutonomousDriver(runtime,RuntimePersistence(),str(path)).run()
    assert path.exists()
    assert run.completed==1
    restored=CognitiveRuntime()
    RuntimePersistence().restore(restored,path,lambda task: (lambda: task.result))
    assert restored.objectives.get(objective.objective_id).status.value=="completed"
