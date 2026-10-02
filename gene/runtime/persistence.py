"""Durable runtime snapshots for pause, crash recovery and continuation."""
from __future__ import annotations
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any
from .cognitive import CognitiveRuntime

class RuntimePersistence:
    VERSION=1

    @staticmethod
    def _jsonable(value: Any) -> Any:
        if value is None or isinstance(value,(str,int,float,bool)): return value
        if isinstance(value,(list,tuple)): return [RuntimePersistence._jsonable(x) for x in value]
        if isinstance(value,dict): return {str(k):RuntimePersistence._jsonable(v) for k,v in value.items()}
        if hasattr(value,"value") and not callable(value.value): return value.value
        return repr(value)

    def save(self,runtime:CognitiveRuntime,path:str|Path)->None:
        payload={
            "version":self.VERSION,
            "objectives":[{"id":o.objective_id,"description":o.description,"status":o.status.value,
                           "parent_id":o.parent_id,"dependencies":sorted(o.dependencies),
                           "additions":o.additions[:],"constraints":o.constraints[:],"metadata":self._jsonable(o.metadata),
                           "version":o.version} for o in runtime.objectives.objectives.values()],
            "tasks":[{"id":t.task_id,"objective":t.objective,"status":t.status.value,
                      "dependencies":sorted(t.dependencies),"metadata":self._jsonable(t.metadata),
                      "result":self._jsonable(t.result),"error":t.error} for t in runtime.graph.tasks.values()]
        }
        target=Path(path);target.parent.mkdir(parents=True,exist_ok=True)
        tmp=target.with_suffix(target.suffix+".tmp")
        tmp.write_text(json.dumps(payload,separators=(",",":")),encoding="utf-8");tmp.replace(target)

    def load_state(self,path:str|Path)->dict[str,Any]:
        data=json.loads(Path(path).read_text(encoding="utf-8"))
        if int(data.get("version",0))!=self.VERSION: raise ValueError("unsupported runtime snapshot version")
        return data

    def restore(self,runtime:CognitiveRuntime,path:str|Path,resolve_operation):
        data=self.load_state(path)
        from gene.objectives.model import Objective, ObjectiveStatus
        from gene.tasks.task import Task, TaskStatus
        runtime.objectives.objectives.clear(); runtime.graph.tasks.clear(); runtime._operations.clear()
        for raw in data["objectives"]:
            objective=Objective(description=raw["description"],objective_id=raw["id"],status=ObjectiveStatus(raw["status"]),parent_id=raw["parent_id"],dependencies=set(raw["dependencies"]),additions=list(raw["additions"]),constraints=list(raw["constraints"]),metadata=dict(raw["metadata"]),version=int(raw["version"]))
            runtime.objectives.objectives[objective.objective_id]=objective
        for raw in data["tasks"]:
            task=Task(objective=raw["objective"],task_id=raw["id"],status=TaskStatus(raw["status"]),dependencies=set(raw["dependencies"]),metadata=dict(raw["metadata"]),result=raw["result"],error=raw["error"])
            runtime.graph.add(task); runtime._operations[task.task_id]=resolve_operation(task)
        return runtime
