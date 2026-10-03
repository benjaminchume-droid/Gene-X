"""Durable runtime checkpointing with atomic writes and recovery validation."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,os,tempfile
from typing import Any,Callable

class DurableRuntime:
    def __init__(self,root:str|Path)->None:
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
        self.path=self.root/"runtime.json"; self.integrity=self.root/"runtime.sha256"

    def checkpoint(self,state:dict[str,Any])->None:
        raw=json.dumps(state,sort_keys=True,separators=(",",":"),default=str)
        digest=hashlib.sha256(raw.encode()).hexdigest()
        fd,tmp=tempfile.mkstemp(dir=self.root,prefix=".runtime-",text=True)
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as f: f.write(raw); f.flush(); os.fsync(f.fileno())
            os.replace(tmp,self.path); self.integrity.write_text(digest,encoding="utf-8")
        finally:
            if os.path.exists(tmp): os.unlink(tmp)

    def restore(self)->dict[str,Any]|None:
        if not self.path.exists() or not self.integrity.exists(): return None
        raw=self.path.read_text(encoding="utf-8")
        if hashlib.sha256(raw.encode()).hexdigest()!=self.integrity.read_text(encoding="utf-8").strip(): raise ValueError("runtime checkpoint integrity failure")
        return json.loads(raw)

    def recover(self, factory:Callable[[dict[str,Any]],Any])->Any|None:
        state=self.restore()
        return None if state is None else factory(state)
