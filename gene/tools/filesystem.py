from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from gene.execution.filesystem import Workspace
@dataclass(frozen=True)
class FilesystemTool:
    workspace: Workspace
    def read(self, path:str)->str: return self.workspace.read_text(path)
    def write(self, path:str, content:str)->None: self.workspace.write_text(path, content)
    def exists(self,path:str)->bool: return self.workspace.exists(path)
    def list(self,path:str="."): return self.workspace.list(path)
