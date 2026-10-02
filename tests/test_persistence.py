from gene.brain import GeneBrain, StructuredExample
from gene.brain.persistence import load_brain, save_brain


def test_brain_checkpoint_round_trip(tmp_path):
    path = tmp_path / "brain.json"
    brain = GeneBrain(input_size=128, hidden_size=8, seed=3)
    brain.train([(StructuredExample(concepts=("dog",)), "animal")], epochs=2)
    save_brain(brain, path)
    restored = load_brain(path)
    assert restored.labels == brain.labels
    assert restored.w1 == brain.w1
    assert restored.predict(StructuredExample(concepts=("dog",))).label == "animal"
