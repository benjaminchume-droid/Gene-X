"""Terminal execution with explicit timeout and working-directory controls."""
from __future__ import annotations
import subprocess
from dataclasses import dataclass

@dataclass(frozen=True)
class TerminalResult:
    code: int
    stdout: str
    stderr: str

class Terminal:
    def __init__(self, timeout: float = 30.0) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.timeout = timeout

    def run(self, argv: list[str], cwd: str | None = None) -> TerminalResult:
        if not argv:
            raise ValueError("argv must not be empty")
        result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=self.timeout)
        return TerminalResult(result.returncode, result.stdout, result.stderr)
