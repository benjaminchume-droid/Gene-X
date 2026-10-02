"""General learned world-dynamics layer over observed numeric transitions."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from gene.brain.predictive import PredictiveCore

@dataclass(frozen=True, slots=True)
class WorldPrediction:
    state: tuple[float,...]
    uncertainty: tuple[float,...]
    source: str="learned"

@dataclass
class LearnedWorldModel:
    state_size:int
    action_size:int
    model:PredictiveCore=field(init=False)
    residuals:list[tuple[float,...]]=field(default_factory=list)

    def __post_init__(self)->None:
        self.model=PredictiveCore(self.state_size,self.action_size,self.state_size)

    def observe(self,before:Iterable[float],action:Iterable[float],after:Iterable[float])->float:
        before=tuple(before); action=tuple(action); after=tuple(after)
        prediction=self.model.predict(before,action)
        residual=tuple(a-p for a,p in zip(after,prediction))
        self.residuals.append(residual)
        self.model.fit([(before,action,after)],epochs=1,learning_rate=0.01)
        return sum(x*x for x in residual)/max(1,len(residual))

    def predict(self,state:Iterable[float],action:Iterable[float])->WorldPrediction:
        values=self.model.predict(state,action)
        if not self.residuals:
            uncertainty=tuple(1.0 for _ in values)
        else:
            uncertainty=tuple(
                (sum(r[i]*r[i] for r in self.residuals)/len(self.residuals))**0.5
                for i in range(len(values))
            )
        return WorldPrediction(values,uncertainty)

    def counterfactual(self,state:Iterable[float],actions:Iterable[Iterable[float]])->tuple[WorldPrediction,...]:
        return tuple(self.predict(state,action) for action in actions)
