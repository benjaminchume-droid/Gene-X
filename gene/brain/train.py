"""Command-line training entry point for Gene X structured experience."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any
from .model import GeneBrain
from .representation import StructuredExample
from .persistence import save_brain

def _example(item: dict[str, Any]) -> StructuredExample:
    return StructuredExample(
        concepts=tuple(str(x) for x in item.get("concepts", ())),
        relations=tuple(tuple(str(x) for x in r) for r in item.get("relations", ())),
        properties=tuple(tuple(r) for r in item.get("properties", ())),
        state=tuple(tuple(r) for r in item.get("state", ())),
        context=tuple(str(x) for x in item.get("context", ())),
    )

def train_file(input_path, output_path, *, mode="representation", epochs=1, learning_rate=0.01,
               input_size=8192, embedding_size=48, representation_size=128):
    records=[json.loads(line) for line in Path(input_path).read_text(encoding="utf-8").splitlines() if line.strip()]
    brain=GeneBrain(input_size=input_size, embedding_size=embedding_size, representation_size=representation_size)
    if mode=="representation":
        report=brain.train_representation([_example(r) for r in records], epochs=epochs, learning_rate=learning_rate)
        result={"mode":mode,"steps":report.steps,"loss":report.mean_loss}
    else:
        pairs=[(_example(r),str(r["target"])) for r in records if "target" in r]
        if not pairs: raise ValueError("supervised mode requires target fields")
        losses=brain.train(pairs, epochs=epochs, learning_rate=learning_rate)
        result={"mode":mode,"epochs":epochs,"losses":losses,"samples":len(pairs)}
    save_brain(brain, output_path)
    return result

def main():
    parser=argparse.ArgumentParser(description="Train Gene X from structured JSONL experience.")
    parser.add_argument("input"); parser.add_argument("output")
    parser.add_argument("--mode",choices=("representation","supervised"),default="representation")
    parser.add_argument("--epochs",type=int,default=1); parser.add_argument("--learning-rate",type=float,default=0.01)
    parser.add_argument("--input-size",type=int,default=8192); parser.add_argument("--embedding-size",type=int,default=48)
    parser.add_argument("--representation-size",type=int,default=128)
    a=parser.parse_args()
    print(json.dumps(train_file(a.input,a.output,mode=a.mode,epochs=a.epochs,learning_rate=a.learning_rate,
        input_size=a.input_size,embedding_size=a.embedding_size,representation_size=a.representation_size)))

if __name__=="__main__":
    main()
