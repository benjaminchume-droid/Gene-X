from gene.brain import BrainTrainer, GeneBrain, StructuredExample, TrainingSample, LongTaskController
from gene.substrate.composition import compose
from gene.substrate.ontology import Entity, Property, WorldModel
from gene.substrate.uncertainty import Belief
from gene.learning.datasets import Dataset, Sample
from gene.learning.generalization import GeneralizationCase, evaluate_generalization


def test_structured_brain_learns_without_token_sequences():
    brain = GeneBrain(input_size=256, hidden_size=16, seed=1)
    samples = [
        TrainingSample(StructuredExample(concepts=("class_a",), properties=(("item_a", "kind", "group_a"),)), "group_a"),
        TrainingSample(StructuredExample(concepts=("class_b",), properties=(("item_b", "kind", "group_a"),)), "group_a"),
        TrainingSample(StructuredExample(concepts=("class_c",), properties=(("item_c", "kind", "group_b"),)), "group_b"),
        TrainingSample(StructuredExample(concepts=("class_d",), properties=(("item_d", "kind", "group_b"),)), "group_b"),
    ]
    report = BrainTrainer(brain).fit(samples, epochs=4, learning_rate=0.08)
    assert report.samples == 4
    assert report.losses[-1] <= report.losses[0]


def test_long_task_survives_plan_changes():
    controller = LongTaskController("objective-1")
    first = controller.add_work("step-a")
    second = controller.add_work("step-b", dependencies={first.work_id})
    controller.complete(first.work_id)
    controller.amend("step-c")
    assert any(item.description == "step-c" for item in controller.items.values())
    assert second in controller.ready()


def test_world_model_is_domain_neutral():
    world = WorldModel()
    entity = world.add_entity(Entity("object"))
    world.add_property(Property(entity.entity_id, "attribute", "value"))
    assert len(world.properties_of(entity.entity_id)) == 1
    assert Belief(("attribute", "value"), 0.8).confidence == 0.8


def test_composition_and_structural_generalization_are_generic():
    value = compose("part-a", "part-b", mode="combined")
    assert dict(value.attributes)["mode"] == "combined"
    report = evaluate_generalization(
        lambda x: x["left"] + x["right"],
        [GeneralizationCase({"left": 2, "right": 3}, 5)],
    )
    assert report.rate == 1.0


def test_dataset_is_streamable():
    dataset = Dataset([Sample("input-a", "target-a"), Sample("input-b", "target-b")])
    assert [x.target for x in dataset.batch(2).__next__()] == ["target-a", "target-b"]
