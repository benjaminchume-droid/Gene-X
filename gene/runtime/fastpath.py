"""Generic fast-path routing for exact and directly registered operations."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Iterable
from gene.computation.arithmetic import add, subtract, multiply, divide

@dataclass(frozen=True, slots=True)
class FastPathResult:
    handled: bool
    value: Any=None
    operation: str|None=None
    confidence: float=0.0

@dataclass(frozen=True, slots=True)
class OperationSpec:
    name: str
    matcher: Callable[[Any], bool]
    execute: Callable[[Any], Any]

class FastPathRegistry:
    def __init__(self, specs: Iterable[OperationSpec]=()) -> None:
        self._specs: dict[str,OperationSpec]={}
        for spec in specs: self.register(spec)
    def register(self,spec:OperationSpec)->None:
        if not spec.name: raise ValueError("operation name cannot be empty")
        if spec.name in self._specs: raise ValueError(f"operation already registered: {spec.name}")
        self._specs[spec.name]=spec
    def route(self,input_value:Any)->FastPathResult:
        for spec in self._specs.values():
            if spec.matcher(input_value): return FastPathResult(True,spec.execute(input_value),spec.name,1.0)
        return FastPathResult(False)

def _arithmetic_request(value: Any) -> bool:
    return isinstance(value,dict) and value.get("kind")=="arithmetic" and value.get("operator") in {"+","-","*","/"}

def _arithmetic_execute(value: dict[str,Any]) -> Any:
    op=value["operator"]; values=tuple(value.get("values",()))
    if not values: raise ValueError("arithmetic request has no values")
    if op=="+": return add(*values)
    if op=="*": return multiply(*values)
    if len(values)!=2: raise ValueError("binary arithmetic requires two values")
    return subtract(*values) if op=="-" else divide(*values)

def default_fast_path() -> FastPathRegistry:
    return FastPathRegistry((OperationSpec("exact-arithmetic",_arithmetic_request,_arithmetic_execute),))
