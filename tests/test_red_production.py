from gene.cognition.metacognition import CognitiveOperation, MetacognitiveController, OperationOutcome
from gene.world.predictive import LearnedWorldModel
from gene.training.synchronize import average_state_dicts
from gene.training.dataset import DatasetCatalog
from benchmarks.datasets import BenchmarkDataset, BenchmarkRecord

def test_metacognition_learns_operation_value():
    c=MetacognitiveController()
    c.register(CognitiveOperation("a",lambda:1)); c.register(CognitiveOperation("b",lambda:2))
    c.learn(OperationOutcome("a","x",0.0)); c.learn(OperationOutcome("b","x",1.0))
    assert c.choose("x").name=="b"

def test_world_model_produces_prediction_and_counterfactuals():
    model=LearnedWorldModel(1,1)
    model.observe((0.1,),(0.2,),(0.3,))
    prediction=model.predict((0.1,),(0.2,))
    alternatives=model.counterfactual((0.1,),((0.2,),(0.8,)))
    assert len(prediction.state)==1 and len(prediction.uncertainty)==1
    assert len(alternatives)==2

def test_distributed_state_aggregation():
    state=average_state_dicts([{"w":[[1.0,3.0]],"b":[2.0]},{"w":[[3.0,5.0]],"b":[4.0]}])
    assert state["w"]==[[2.0,4.0]] and state["b"]==[3.0]

def test_benchmark_partition_is_reproducible():
    data=BenchmarkDataset([BenchmarkRecord(str(i),i) for i in range(6)])
    assert [x.case_id for x in data.partition(0,2)]==["0","2","4"]
