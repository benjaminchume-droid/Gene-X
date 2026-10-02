"""Versioned dataset catalog with content-addressed manifests."""
from __future__ import annotations
from dataclasses import dataclass,field
from pathlib import Path
from .dataset import DatasetManifest, JsonlDatasetBuilder

@dataclass
class DatasetCatalog:
    manifests: dict[tuple[str,str],DatasetManifest]=field(default_factory=dict)

    def register_jsonl(self,path:str|Path,*,dataset_id:str,version:str,schema:str="generic")->DatasetManifest:
        manifest=JsonlDatasetBuilder(path).manifest(dataset_id=dataset_id,version=version,schema=schema)
        key=(dataset_id,version)
        existing=self.manifests.get(key)
        if existing and existing.source!=manifest.source: raise ValueError("dataset version already registered with different content")
        self.manifests[key]=manifest
        return manifest

    def get(self,dataset_id:str,version:str)->DatasetManifest:
        return self.manifests[(dataset_id,version)]
