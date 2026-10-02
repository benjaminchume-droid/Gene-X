from benchmarks.runner import BenchmarkCase
import json
from pathlib import Path
def load(path)->tuple[BenchmarkCase,...]:
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(BenchmarkCase(x["case_id"],x.get("input"),x.get("expected"),x.get("metadata")) for x in data)
