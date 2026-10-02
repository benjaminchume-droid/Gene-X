from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class ModalInput:
    modality:str; value:Any; metadata:dict[str,Any]=None
@dataclass(frozen=True)
class FusedRepresentation:
    parts:tuple[ModalInput,...]
    shared:Any=None
class FusionEngine:
    def fuse(self,inputs:list[ModalInput])->FusedRepresentation:
        if not inputs: raise ValueError("at least one input is required")
        return FusedRepresentation(tuple(inputs))
