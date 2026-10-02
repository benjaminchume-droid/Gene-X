"""External benchmark dataset loading and validation."""
from __future__ import annotations
import json
from pathlib import Path
from .datasets import BenchmarkDataset, BenchmarkRecord

def load_jsonl(path:str|Path,*,version:str="1")->BenchmarkDataset:
    records=[]
    with Path(path).open("r",encoding="utf-8") as handle:
        for line in handle:
            if not line.strip(): continue
            item=json.loads(line)
            if "case_id" not in item or "input" not in item: raise ValueError("benchmark record requires case_id and input")
            records.append(BenchmarkRecord(str(item["case_id"]),item["input"],item.get("expected"),dict(item.get("metadata",{}))))
    return BenchmarkDataset(records,version=version)
