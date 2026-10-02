from gene.brain import GeneBrain, StructuredExample
from gene.brain.persistence import load_brain, save_brain


def test_brain_checkpoint_round_trip(tmp_path):
    path = tmp_path / "brain.json"
    brain = GeneBrain(input_size=128, representation_size=16, embedding_size=8, seed=3)
    brain.train_representation([StructuredExample(concepts=("synthetic-a",))], epochs=2)
    save_brain(brain, path)
    restored = load_brain(path)
    assert restored.representation.state_dict() == brain.representation.state_dict()
