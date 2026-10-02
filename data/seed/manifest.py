"""Seed-data manifest. Actual seed records are supplied externally."""
from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SeedManifest:
    source:str
    version:str
    record_count:int
