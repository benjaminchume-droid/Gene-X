from gene.system import GeneSystem

def test_complete_system_exposes_core_capabilities():
    gene=GeneSystem()
    caps=gene.capabilities()
    assert caps.representation and caps.memory and caps.reasoning
    assert caps.generation and caps.autonomy and caps.training and caps.security

def test_chat_requires_real_backend_instead_of_simulating():
    gene=GeneSystem()
    try:
        gene.chat("hello")
    except RuntimeError as exc:
        assert "language generation backend" in str(exc)
    else:
        raise AssertionError("Gene must not fabricate a chat response")

def test_perception_is_provider_driven():
    gene=GeneSystem()
    class Provider:
        modality="x"
        def perceive(self,input_data,*,context=None): return {"representation":input_data}
    gene.perception.register(Provider())
    observation=gene.perceive("x",123)
    assert observation.representation=={"representation":123}
