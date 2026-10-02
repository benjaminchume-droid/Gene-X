from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class GenerationRequest:
    modality:str;prompt:Any;parameters:dict[str,Any]|None=None
class Generator(ABC):
    @abstractmethod
    def generate(self,request:GenerationRequest)->Any:...
