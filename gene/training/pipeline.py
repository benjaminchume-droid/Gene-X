"""Canonical training pipeline: data -> representation -> model -> update -> checkpoint -> evaluation."""
from __future__ import annotations
from dataclasses import dataclass
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
        self.model=model; self.config=config; self.checkpoint_dir=Path(checkpoint_dir); self.checkpoint_dir.mkdir(parents=True,exist_ok=True)
        self.step=0

    def _save(self, metrics:TrainingMetrics)->str:
        payload={"version":1,"config":self.config.__dict__,"step":self.step,"metrics":metrics.__dict__,"model":self.model.state_dict()}
        raw=json.dumps(payload,sort_keys=True,separators=(",",":"))
        digest=hashlib.sha256(raw.encode()).hexdigest()
        path=self.checkpoint_dir/f"{self.config.run_id}-{self.step}.json"
        path.write_text(json.dumps({"sha256":digest,"payload":payload},sort_keys=True),encoding="utf-8")
        return str(path)

    def train(self, batches:Iterable[Sequence[tuple[Iterable[Iterable[float]],Iterable[float]]]], *, evaluator:Callable[[Any],float]|None=None)->TrainingReport:
        started=time.time(); metrics=[]; latest=None
        for _ in range(self.config.epochs):
            for batch in batches:
                result=self.model.fit(batch,epochs=1,learning_rate=self.config.learning_rate)
                self.step+=result.samples
                loss=result.loss
                if evaluator is not None: evaluator(self.model)
                m=TrainingMetrics(self.step,loss,time.time()-started); metrics.append(m)
                if self.step % self.config.checkpoint_every==0: latest=self._save(m)
        if metrics and latest is None: latest=self._save(metrics[-1])
        return TrainingReport(self.config.run_id,self.step,tuple(metrics),latest)

    def resume(self,path:str|Path)->TrainingMetrics:
        item=json.loads(Path(path).read_text(encoding="utf-8"))
        payload=item["payload"]; raw=json.dumps(payload,sort_keys=True,separators=(",",":"))
        if hashlib.sha256(raw.encode()).hexdigest()!=item["sha256"]: raise ValueError("checkpoint integrity failure")
        self.step=int(payload["step"]); self.model.load_state_dict(payload["model"])
        m=payload["metrics"]; return TrainingMetrics(int(m["step"]),float(m["loss"]),float(m["elapsed"]))
