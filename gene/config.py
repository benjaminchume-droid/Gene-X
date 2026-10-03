from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os,json
@dataclass(frozen=True,slots=True)
class GenePaths: root:Path; data:Path; models:Path; runs:Path; config:Path
def default_paths():
 r=Path(os.environ.get('GENE_HOME',str(Path.home()/'.gene'))); return GenePaths(r,r/'data',r/'models',r/'runs',r/'config')
def ensure_paths(p=None):
 p=p or default_paths()
 for x in (p.root,p.data,p.models,p.runs,p.config): x.mkdir(parents=True,exist_ok=True)
 return p
def load_config(p=None):
 f=ensure_paths(p).config/'gene.json'; return json.loads(f.read_text()) if f.exists() else {}
