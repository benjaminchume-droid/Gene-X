from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class ModalInput:
    modality:str;value:Any;metadata:dict[str,Any]|None=None
@dataclass(frozen=True)
class FusedRepresentation:
    parts:tuple[ModalInput,...];shared:Any=None
class FusionEngine:
    def fuse(self,inputs:list[ModalInput])->FusedRepresentation:
        if not inputs:raise ValueError("at least one input is required")
        return FusedRepresentation(tuple(inputs))
