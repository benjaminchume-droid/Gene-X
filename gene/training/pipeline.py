"""Canonical training pipeline with deterministic manifests and resumable checkpoints."""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib,json,time
from pathlib import Path
from typing import Callable, Iterable, Sequence, Any

@dataclass(frozen=True, slots=True)
class TrainingConfig:
    run_id:str
    epochs:int=1
    learning_rate:float=.001
    checkpoint_every:int=100
    seed:int=7

@dataclass(frozen=True, slots=True)
class TrainingMetrics:
    step:int
    loss:float
    elapsed:float

@dataclass(frozen=True, slots=True)
class TrainingReport:
    run_id:str
    steps:int
    metrics:tuple[TrainingMetrics,...]
    checkpoint:str|None

class TrainingPipeline:
    def __init__(self, model:Any, checkpoint_dir:str|Path, config:TrainingConfig) -> None:
        if config.epochs<1 or config.learning_rate<=0 or config.checkpoint_every<1: raise ValueError("invalid training configuration")
        self.model=model; self.config=config; self.checkpoint_dir=Path(checkpoint_dir); self.checkpoint_dir.mkdir(parents=True,exist_ok=True)
        self.step=0

    def _save(self, metrics:TrainingMetrics)->str:
        payload={"version":2,"config":asdict(self.config),"step":self.step,"metrics":asdict(metrics),"model":self.model.state_dict()}
        raw=json.dumps(payload,sort_keys=True,separators=(",",":"),allow_nan=False)
        digest=hashlib.sha256(raw.encode()).hexdigest()
        path=self.checkpoint_dir/f"{self.config.run_id}-{self.step}.json"
        tmp=path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"sha256":digest,"payload":payload},sort_keys=True),encoding="utf-8")
        tmp.replace(path)
        return str(path)

    def train(self, batches:Iterable[Sequence[tuple[Iterable[Iterable[float]],Iterable[float]]]], *, evaluator:Callable[[Any],float]|None=None)->TrainingReport:
        started=time.time(); metrics=[]; latest=None
        for _ in range(self.config.epochs):
            for batch in batches:
                result=self.model.fit(batch,epochs=1,learning_rate=self.config.learning_rate)
                self.step+=result.samples
                m=TrainingMetrics(self.step,float(result.loss),time.time()-started); metrics.append(m)
                if evaluator is not None: evaluator(self.model)
                if self.step % self.config.checkpoint_every==0: latest=self._save(m)
        if metrics and latest is None: latest=self._save(metrics[-1])
        return TrainingReport(self.config.run_id,self.step,tuple(metrics),latest)

    def resume(self,path:str|Path)->TrainingMetrics:
        item=json.loads(Path(path).read_text(encoding="utf-8"))
        payload=item["payload"]; raw=json.dumps(payload,sort_keys=True,separators=(",",":"),allow_nan=False)
        if hashlib.sha256(raw.encode()).hexdigest()!=item["sha256"]: raise ValueError("checkpoint integrity failure")
        if int(payload.get("version",0))<1: raise ValueError("unsupported checkpoint")
        self.step=int(payload["step"]); self.model.load_state_dict(payload["model"])
        m=payload["metrics"]; return TrainingMetrics(int(m["step"]),float(m["loss"]),float(m["elapsed"]))
