"""Executable foundation-substrate training entrypoint.

The dataset is external JSONL. Each record must contain:
{"input": [[...], [...]], "target": [...]}
No training examples are embedded in the implementation.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path
from gene.foundation import UniversalFoundationModel
from gene.training.dataset import JsonlDatasetBuilder
from gene.training.pipeline import TrainingConfig,TrainingPipeline

def load_batches(path:str,batch_size:int):
    records=JsonlDatasetBuilder(path).records()
    batch=[]
    for record in records:
        batch.append((record.value,record.target))
        if len(batch)>=batch_size:
            yield tuple(batch); batch=[]
    if batch: yield tuple(batch)

def main(argv=None)->int:
    p=argparse.ArgumentParser()
    p.add_argument("dataset"); p.add_argument("--input-size",type=int,required=True)
    p.add_argument("--hidden-size",type=int,default=64); p.add_argument("--epochs",type=int,default=1)
    p.add_argument("--learning-rate",type=float,default=.001); p.add_argument("--batch-size",type=int,default=4)
    p.add_argument("--checkpoint-dir",default="checkpoints"); p.add_argument("--run-id",default="foundation")
    a=p.parse_args(argv)
    model=UniversalFoundationModel(a.input_size,a.hidden_size)
    config=TrainingConfig(a.run_id,a.epochs,a.learning_rate)
    report=TrainingPipeline(model,a.checkpoint_dir,config).train(load_batches(a.dataset,a.batch_size))
    print(json.dumps({"run_id":report.run_id,"steps":report.steps,"loss":[m.loss for m in report.metrics],"checkpoint":report.checkpoint}))
    return 0

if __name__=="__main__": raise SystemExit(main())
