from gene.brain.representation import StructuredExample, encode_structure

def test_representation_has_no_domain_knowledge():
    empty=encode_structure(StructuredExample())
    arbitrary=encode_structure(StructuredExample(concepts=("x",),properties=(("x","k",7),)))
    assert empty.values=={}
    assert arbitrary.values
