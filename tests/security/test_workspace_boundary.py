import pytest
from gene.execution.filesystem import Workspace
def test_workspace_rejects_escape(tmp_path):
    ws=Workspace(tmp_path)
    with pytest.raises(PermissionError): ws.path("../outside")
