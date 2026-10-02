from __future__ import annotations
import subprocess
from dataclasses import dataclass
@dataclass(frozen=True)
class GitTool:
    root:str
    def run(self,args:list[str],*,timeout:float=30.0):
        p=subprocess.run(["git",*args],cwd=self.root,text=True,capture_output=True,timeout=timeout,check=False)
        return {"returncode":p.returncode,"stdout":p.stdout,"stderr":p.stderr}
