"""Execution sandbox boundary using an injected policy."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Protocol

class SandboxPolicy(Protocol):
    def allow(self, operation: str, context: dict[str, Any]) -> bool: ...

@dataclass
class Sandbox:
    policy: SandboxPolicy

    def execute(self, operation: str, action: Callable[[], Any], **context: Any) -> Any:
        if not self.policy.allow(operation, context):
            raise PermissionError(f"sandbox policy denied operation: {operation}")
        return action()
