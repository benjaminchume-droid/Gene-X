from gene.training.dataset import JsonlDatasetBuilder
from gene.training.catalog import DatasetCatalog

def test_dataset_manifest_is_content_addressed(tmp_path):
    path=tmp_path/"data.jsonl"
    path.write_text('{"input":1,"target":2}\n',encoding="utf-8")
    catalog=DatasetCatalog()
    manifest=catalog.register_jsonl(path,dataset_id="d",version="1")
    assert manifest.records==1
    assert catalog.get("d","1").source==manifest.source
