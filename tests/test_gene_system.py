from gene import GeneSystem
from gene.tools.registry import Tool

def test_gene_system_composes_core_organs():
    gene=GeneSystem()
    caps=gene.capabilities()
    assert all(getattr(caps,n) for n in caps.__dataclass_fields__)
    assert gene.organism.runtime.learning is not None
    assert gene.health()["objectives"] == 0

def test_tool_is_wired_into_kernel_and_security_boundary():
    gene=GeneSystem()
    gene.security.allowed.add("read")
    gene.register_tool(Tool("probe", lambda value: value + 1, capabilities=frozenset({"read"})))
    assert gene.execute_tool("probe", {"value": 4}) == 5
    assert "tool:probe" in gene.kernel.capabilities.names()
