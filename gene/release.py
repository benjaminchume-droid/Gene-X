"""Production release metadata and readiness gates."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True, slots=True)
class ReleaseGate:
    name:str
    check:Callable[[],bool]

@dataclass(frozen=True, slots=True)
class ReleaseReport:
    ready:bool
    failed:tuple[str,...]

class ReleaseVerifier:
    def verify(self,gates:list[ReleaseGate])->ReleaseReport:
        failed=[]
        for gate in gates:
            try:
                passed=bool(gate.check())
            except Exception:
                passed=False
            if not passed: failed.append(gate.name)
        return ReleaseReport(not failed,tuple(failed))
