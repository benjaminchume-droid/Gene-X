import json
from pathlib import Path
from .schema import RuntimeConfig
def load_json(path): return RuntimeConfig(**json.loads(Path(path).read_text(encoding="utf-8")))
def dump_json(config,path):
    Path(path).write_text(json.dumps({"max_workers":config.max_workers,"step_timeout_seconds":config.step_timeout_seconds,"checkpoint_interval":config.checkpoint_interval,"deterministic":config.deterministic,"metadata":config.metadata},indent=2),encoding="utf-8")
