from gene.runtime.persistence import RuntimePersistence
def test_jsonable_scalars():
    assert RuntimePersistence._jsonable({"x":[1,True]})=={"x":[1,True]}
