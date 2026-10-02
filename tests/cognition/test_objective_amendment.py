from gene.objectives.model import Objective,ObjectiveChange
def test_amendment_is_additive():
    o=Objective("base"); o.amend(ObjectiveChange("detail",additions=("x",),constraints=("y",)))
    assert o.description=="base" and o.additions==["x"] and o.constraints==["y"]
