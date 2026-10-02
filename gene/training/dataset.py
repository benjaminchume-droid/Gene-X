"""Production dataset manifests, validation and deterministic sharding."""
from __future__ import annotations
from dataclasses import dataclass, field
import hashlib, json
from pathlib import Path
from typing import Any, Iterable, Iterator

@dataclass(frozen=True, slots=True)
class DatasetRecord:
    value: Any
    target: Any=None
    metadata: dict[str,Any]=field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class DatasetManifest:
    dataset_id: str
    version: str
    records: int
    schema: str
    source: str

class DatasetShard:
    def __init__(self, records: Iterable[DatasetRecord], rank:int=0, world_size:int=1) -> None:
        if world_size<1 or rank<0 or rank>=world_size: raise ValueError("invalid shard coordinates")
        self.records=tuple(records); self.rank=rank; self.world_size=world_size
    def __iter__(self)->Iterator[DatasetRecord]:
        for index,record in enumerate(self.records):
            if index % self.world_size == self.rank: yield record

class JsonlDatasetBuilder:
    def __init__(self,path:str|Path): self.path=Path(path)
    def manifest(self, *, dataset_id:str, version:str, schema:str="generic")->DatasetManifest:
        count=0
        for line in self.path.open("r",encoding="utf-8"):
            if line.strip(): count+=1
        digest=hashlib.sha256(self.path.read_bytes()).hexdigest()
        return DatasetManifest(dataset_id,version,count,schema,digest)
    def records(self)->Iterator[DatasetRecord]:
        with self.path.open("r",encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    item=json.loads(line)
                    yield DatasetRecord(item.get("input"),item.get("target"),dict(item.get("metadata",{})))
