from gene import Gene
from gene.runtime.latency import CognitiveMode

def test_reflex_path_uses_exact_operation():
    gene=Gene()
    response=gene.think({"kind":"arithmetic","operator":"*","values":(15,7)})
    assert response.value==105
    assert response.mode==CognitiveMode.REFLEX.value

def test_conversational_path_is_distinct():
    gene=Gene()
    response=gene.think("input",complexity=2.0,interpret=lambda x:{"value":x},reason=lambda x,r:{"answer":x["value"]})
    assert response.mode==CognitiveMode.CONVERSATIONAL.value
    assert response.value=={"answer":"input"}

def test_deep_path_is_distinct():
    gene=Gene()
    response=gene.think("objective",complexity=10.0,requires_action=True,reason=lambda x,r:("planned",x))
    assert response.mode==CognitiveMode.DEEP.value
    assert response.value[0]=="planned"
