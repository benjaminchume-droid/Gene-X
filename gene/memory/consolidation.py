"""Memory consolidation from raw experiences into durable records."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from .store import MemoryRecord, MemoryStore

@dataclass(frozen=True,slots=True)
class ConsolidationResult:
    seen:int
    retained:int
    discarded:int

class Consolidator:
    def __init__(self,transform:Callable[[Iterable[Any]],Iterable[Any]]|None=None)->None:
        self.transform=transform or (lambda records:records)

    def consolidate(self,records:Iterable[Any])->list[Any]:
        return list(self.transform(records))

    def commit(self,store:MemoryStore,records:Iterable[MemoryRecord])->ConsolidationResult:
        batch=tuple(records); retained=0
        for record in self.consolidate(batch):
            if not isinstance(record,MemoryRecord): raise TypeError("consolidation must return MemoryRecord values")
            store.put(record); retained+=1
        return ConsolidationResult(len(batch),retained,len(batch)-retained)
