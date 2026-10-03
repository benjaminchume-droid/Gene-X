from gene.multimodal.encoders import NumericImageEncoder,AudioEncoder,VideoEncoder,SpatialEncoder
from gene.multimodal.fusion_learning import LearnedFusion
from gene.generation.engines import TextEngine,ImageEngine,AudioEngine,MusicEngine,VideoEngine,WorldEngine

def test_encoders_extract_real_signal_structure():
    assert NumericImageEncoder().encode([[[1.0],[2.0]]]).vector[-1]==2.0
    assert AudioEncoder().encode([0.0,1.0,-1.0],100).vector[-1]==3.0
    assert VideoEncoder().encode([[[[1.0]]]],1.0).vector[-1]==8.0
    assert SpatialEncoder().encode([(0.0,1.0),(2.0,3.0)]).shape==(2,2)

def test_fusion_learns():
    f=LearnedFusion(2,2)
    before=f.forward(((1.0,0.0),(0.0,1.0)))
    step=f.fit([(((1.0,0.0),(0.0,1.0)),(1.0,1.0))],epochs=2)
    after=f.forward(((1.0,0.0),(0.0,1.0)))
    assert step.samples==2 and before!=after

def test_generation_is_computational():
    assert len(TextEngine().generate(("a","b"),repeat=3).data)==6
    assert len(ImageEngine().generate(2,2,1,(.1,.2)).data)==2
    assert len(AudioEngine().generate(8,100,(2.0,)).data)==8
    assert len(MusicEngine().generate(5,(1.0,2.0)).data)==5
    assert len(VideoEngine().generate(3,2,2,(.1,)).data)==3
    assert WorldEngine().generate(((0.,),(1.,)),((0,1),)).metadata["edge_count"]==1
