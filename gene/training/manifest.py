"""Training run manifests and reproducibility metadata."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
import hashlib,json,platform,sys

@dataclass(frozen=True, slots=True)
class RunManifest:
    run_id:str
    created_at:str
    python:str
    platform:str
    config_hash:str
    dataset_hash:str

def create_manifest(run_id:str,config:dict,dataset_hash:str)->RunManifest:
    raw=json.dumps(config,sort_keys=True,separators=(",",":"))
    return RunManifest(run_id,datetime.now(timezone.utc).isoformat(),sys.version,platform.platform(),hashlib.sha256(raw.encode()).hexdigest(),dataset_hash)
