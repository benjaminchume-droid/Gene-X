from gene.brain import (
    BrainTrainer,
    GeneBrain,
    StructuredExample,
    TrainingSample,
    LongTaskController,
)


def test_structured_brain_learns_without_token_sequences():
    brain = GeneBrain(input_size=256, hidden_size=16, seed=1)
    samples = [
        TrainingSample(StructuredExample(concepts=("dog",), properties=(("dog", "color", "blue"),)), "animal"),
        TrainingSample(StructuredExample(concepts=("cat",), properties=(("cat", "color", "black"),)), "animal"),
        TrainingSample(StructuredExample(concepts=("compiler",), properties=(("compiler", "kind", "tool"),)), "tool"),
        TrainingSample(StructuredExample(concepts=("browser",), properties=(("browser", "kind", "tool"),)), "tool"),
    ]
    report = BrainTrainer(brain).fit(samples, epochs=4, learning_rate=0.08)
    assert report.samples == 4
    assert report.losses[-1] <= report.losses[0]


def test_long_task_survives_plan_changes():
    controller = LongTaskController("objective-1")
    first = controller.add_work("build core")
    second = controller.add_work("build tests", dependencies={first.work_id})
    controller.complete(first.work_id)
    controller.amend("build documentation")
    assert any(item.description == "build documentation" for item in controller.items.values())
    assert second in controller.ready()
