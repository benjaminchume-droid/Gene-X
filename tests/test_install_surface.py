from gene.config import ensure_paths
from gene import GeneSystem
def test_install_surface(tmp_path,monkeypatch):
 monkeypatch.setenv('GENE_HOME',str(tmp_path/'gene')); p=ensure_paths(); assert all(x.exists() for x in (p.root,p.data,p.models,p.runs,p.config)); assert isinstance(GeneSystem(),GeneSystem)
