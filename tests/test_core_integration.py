from gene.runtime.cognitive import CognitiveRuntime
from gene.objectives.model import ObjectiveChange
from gene.memory.store import MemoryStore, MemoryRecord
from gene.memory.retrieval import MemoryRetriever
from gene.consultation.manager import ConsultationManager, ConsultationRequest
from gene.consultation.loop import ConsultativeLoop
from gene.world.inference import WorldReasoner
from gene.substrate.ontology import WorldModel, Entity, Property
from gene.evaluation.suite import EvaluationSuite, EvaluationCase

def test_objective_runtime_survives_amendment_and_executes():
    runtime=CognitiveRuntime()
    objective=runtime.add_objective("persistent objective")
    seen=[]
    first=runtime.add_task(objective,lambda: seen.append("first") or 1)
    runtime.amend_objective(objective.objective_id,ObjectiveChange("add",additions=("new constraint",)))
    second=runtime.add_task(objective,lambda: seen.append("second") or 2,dependencies={first.task_id})
    assert [x.task_id for x in runtime.ready()]==[first.task_id]
    runtime.run_ready()
    assert [x.task_id for x in runtime.ready()]==[second.task_id]
    runtime.run_ready()
    assert seen==["first","second"]
    assert runtime.objectives.get(objective.objective_id).status.value=="completed"

def test_memory_retrieval_and_consultation_are_real_primitives():
    store=MemoryStore()
    store.put(MemoryRecord("a",{"v":1},"experience"))
    store.put(MemoryRecord("b",{"v":2},"experience"))
    encode=lambda value:(float(value["v"]),0.0)
    result=MemoryRetriever(store,encode).query({"v":1},limit=1)
    assert result[0].record.key=="a"

    manager=ConsultationManager()
    manager.register("source",lambda request: {"candidate":request.question})
    loop=ConsultativeLoop(manager,lambda rs:rs[0].answer,
                          lambda candidate: {"ok":candidate["candidate"]},
                          lambda candidate,execution:(execution["ok"]==candidate["candidate"],execution))
    attempt=loop.run(ConsultationRequest("x"))
    assert attempt.verified

def test_world_reasoning_and_evaluation():
    world=WorldModel()
    entity=world.add_entity(Entity("runtime"))
    world.add_property(Property(entity.entity_id,"state","ready",0.9,"source"))
    inferred=WorldReasoner(world).infer_property(entity.entity_id,"state")
    assert inferred is not None and inferred.value=="ready"
    report=EvaluationSuite([EvaluationCase("case",lambda:3,lambda x:1.0)]).run()
    assert report.score==1.0


def test_autonomous_driver_drains_ready_work():
    from gene.runtime.autonomous import AutonomousDriver
    runtime=CognitiveRuntime()
    objective=runtime.add_objective("autonomous")
    runtime.add_task(objective,lambda:1)
    report=AutonomousDriver(runtime).run()
    assert report.completed==1
    assert not runtime.ready()


def test_runtime_snapshot_round_trip(tmp_path):
    from gene.runtime.persistence import RuntimePersistence
    runtime=CognitiveRuntime()
    objective=runtime.add_objective("persisted")
    task=runtime.add_task(objective,lambda:7)
    path=tmp_path/"runtime.json"
    RuntimePersistence().save(runtime,path)
    restored=CognitiveRuntime()
    RuntimePersistence().restore(restored,path,lambda t: (lambda:7))
    assert restored.objectives.get(objective.objective_id).description=="persisted"
    assert restored.graph.tasks[task.task_id].result is None
    assert restored.graph.tasks[task.task_id].status.value=="pending"
