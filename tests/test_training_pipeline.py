from pathlib import Path
import json
from gene.foundation import UniversalFoundationModel
from gene.training.pipeline import TrainingConfig,TrainingPipeline

def test_training_pipeline_updates_and_resumes(tmp_path:Path):
    model=UniversalFoundationModel(2,4,seed=3)
    target=(.2,-.1,.3,.4)
    batches=[(((1.0,0.0),(0.0,1.0)),target),(((.5,.5),(-.5,.2)),target)]
    p=TrainingPipeline(model,tmp_path,TrainingConfig("smoke",epochs=1,checkpoint_every=1))
    report=p.train([batches[0]])
    assert report.steps==1 and report.checkpoint
    restored=UniversalFoundationModel(2,4,seed=99)
    resumed=TrainingPipeline(restored,tmp_path,TrainingConfig("resume",checkpoint_every=1))
    metric=resumed.resume(report.checkpoint)
    assert metric.step==1

def test_checkpoint_detects_tampering(tmp_path:Path):
    model=UniversalFoundationModel(1,2)
    p=TrainingPipeline(model,tmp_path,TrainingConfig("integrity"))
    report=p.train([(((1.0,),),(.1,.2))])
    path=Path(report.checkpoint)
    item=json.loads(path.read_text())
    item["payload"]["step"]=999
    path.write_text(json.dumps(item))
    try: p.resume(path)
    except ValueError: pass
    else: raise AssertionError("tampered checkpoint was accepted")
