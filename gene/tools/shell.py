from dataclasses import dataclass
from gene.execution.terminal import Terminal, TerminalResult
@dataclass(frozen=True)
class ShellTool:
    terminal: Terminal
    def run(self, command:list[str], *, timeout:float=30.0, cwd=None)->TerminalResult:
        return self.terminal.run(command, timeout=timeout, cwd=cwd)
