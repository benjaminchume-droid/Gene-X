from __future__ import annotations
import subprocess
from dataclasses import dataclass
@dataclass(frozen=True)
class CompilerTool:
    command: tuple[str,...] = ("python","-m","compileall")
    def compile(self,target:str,*,timeout:float=120.0):
        p=subprocess.run([*self.command,target],text=True,capture_output=True,timeout=timeout,check=False)
        return {"success":p.returncode==0,"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
