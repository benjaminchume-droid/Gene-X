"""Transport-neutral request/response protocol for Gene runtimes."""
from __future__ import annotations
from dataclasses import dataclass,field
from typing import Any
from uuid import uuid4
@dataclass(frozen=True)
class GeneRequest:
    operation:str
    payload:dict[str,Any]=field(default_factory=dict)
    id:str=field(default_factory=lambda:str(uuid4()))
@dataclass(frozen=True)
class GeneResponse:
    request_id:str
    success:bool
    payload:Any=None
    error:str|None=None
class ProtocolHandler:
    def __init__(self,operations:dict[str,Any]|None=None):self.operations=operations or {}
    def handle(self,request:GeneRequest)->GeneResponse:
        operation=self.operations.get(request.operation)
        if operation is None:return GeneResponse(request.id,False,error=f"unknown operation: {request.operation}")
        try:return GeneResponse(request.id,True,payload=operation(request.payload))
        except Exception as exc:return GeneResponse(request.id,False,error=str(exc))
