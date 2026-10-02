"""Thread-safe objective injection for long-running runtimes."""
from __future__ import annotations
from dataclasses import dataclass
from queue import SimpleQueue
from typing import Any

@dataclass(frozen=True, slots=True)
class ObjectiveMessage:
    description:str
    metadata:dict[str,Any]

class ObjectiveInbox:
    def __init__(self)->None: self._queue=SimpleQueue()
    def submit(self,description:str,**metadata:Any)->None:
        self._queue.put(ObjectiveMessage(description,dict(metadata)))
    def drain(self)->tuple[ObjectiveMessage,...]:
        items=[]
        while not self._queue.empty():
            items.append(self._queue.get())
        return tuple(items)
