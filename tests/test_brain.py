from gene.brain import (
    BrainTrainer,
    GeneBrain,
    StructuredExample,
    TrainingSample,
    LongTaskController,
    CognitionCycle,
    CycleAction,
    CycleEvaluation,
    CycleObservation,
)


def test_structured_brain_learns_without_token_sequences():
    brain = GeneBrain(input_size=256, representation_size=24, embedding_size=12, seed=1)
    samples = [
        TrainingSample(StructuredExample(concepts=("synthetic-a",)), "group-a"),
        TrainingSample(StructuredExample(concepts=("synthetic-b",)), "group-a"),
        TrainingSample(StructuredExample(concepts=("synthetic-c",)), "group-b"),
        TrainingSample(StructuredExample(concepts=("synthetic-d",)), "group-b"),
    ]
    report = BrainTrainer(brain).fit(samples, epochs=4, learning_rate=0.08)
    assert report.samples == 4
    assert report.losses[-1] <= report.losses[0]


def test_representation_is_trainable_without_labels():
    brain = GeneBrain(input_size=256, representation_size=24, embedding_size=12, seed=2)
    examples = [
        StructuredExample(concepts=("synthetic-a",), properties=(("x", "v", 1),)),
        StructuredExample(concepts=("synthetic-b",), properties=(("x", "v", 2),)),
    ]
    report = brain.train_representation(examples, epochs=2)
    assert report.steps == 4
    assert brain.representation.training_steps == 4


def test_long_task_survives_plan_changes():
    controller = LongTaskController("objective-1")
    first = controller.add_work("step-a")
    second = controller.add_work("step-b", dependencies={first.work_id})
    controller.complete(first.work_id)
    controller.amend("step-c")
    assert any(item.description == "step-c" for item in controller.items.values())
    assert second in controller.ready()


def test_cycle_observes_acts_verifies_and_learns():
    brain = GeneBrain(input_size=256, representation_size=24, embedding_size=12, seed=4)
    cycle = CognitionCycle(brain=brain)
    observation = CycleObservation(
        value={"signal": 1},
        structure=StructuredExample(concepts=("synthetic-a",)),
    )
    result = cycle.step(
        observation,
        action_selector=lambda *_: CycleAction("synthetic-operation"),
        executor=lambda action: {"completed": action.name},
        evaluator=lambda action, execution, obs: CycleEvaluation(True, 1.0),
    )
    assert result.action is not None
    assert result.evaluation is not None and result.evaluation.passed
    assert result.learned


def test_domain_neutral_primitives():
    brain = GeneBrain(input_size=256, representation_size=24, embedding_size=12)
    assert brain.representation.training_steps == 0
