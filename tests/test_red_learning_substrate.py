from gene.brain.predictive import PredictiveCore
from gene.multimodal.alignment import AlignmentSample, CrossModalAligner

def test_predictive_core_learns_a_generic_numeric_transition():
    core = PredictiveCore(1, 1, 1, seed=1)
    before = core.predict((0.2,), (0.3,))[0]
    core.fit([((0.2,), (0.3,), (0.8,))], epochs=50, learning_rate=0.05)
    after = core.predict((0.2,), (0.3,))[0]
    assert abs(after - 0.8) < abs(before - 0.8)

def test_cross_modal_alignment_is_trainable():
    aligner = CrossModalAligner(2, 2, shared_size=2, seed=1)
    samples = [AlignmentSample((1.0, 0.0), (0.0, 1.0))]
    before = aligner.similarity(samples[0].source, samples[0].target)
    report = aligner.fit(samples, epochs=20, learning_rate=0.01)
    after = aligner.similarity(samples[0].source, samples[0].target)
    assert report.steps == 20
    assert after >= before
