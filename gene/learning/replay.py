from collections import deque
from dataclasses import dataclass
from random import Random

class ReplayBuffer:
    def __init__(self,capacity:int=10000):
        if capacity<1:raise ValueError("capacity must be positive")
        self.capacity=capacity;self._items=deque(maxlen=capacity)
    def add(self,item):self._items.append(item)
    def sample(self,limit:int):return tuple(list(self._items)[-max(0,limit):])
    def __len__(self):return len(self._items)

@dataclass(frozen=True)
class ReplayItem:
    experience: object
    priority: float = 1.0

class PrioritizedReplay:
    def __init__(self,capacity:int=10000,seed:int=7):
        if capacity<1:raise ValueError("capacity must be positive")
        self.capacity=capacity; self._rng=Random(seed); self._items:list[ReplayItem]=[]
    def add(self,experience,priority:float=1.0)->None:
        self._items.append(ReplayItem(experience,max(0.0,priority)))
        if len(self._items)>self.capacity:
            self._items.sort(key=lambda x:x.priority,reverse=True)
            del self._items[self.capacity:]
    def sample(self,n:int)->tuple[object,...]:
        if n<=0 or not self._items:return ()
        weights=[max(1e-9,x.priority) for x in self._items]
        return tuple(x.experience for x in self._rng.choices(self._items,weights=weights,k=min(n,len(self._items))))
    def __len__(self):return len(self._items)
