from collections import deque
class ReplayBuffer:
    def __init__(self,capacity:int=10000):
        if capacity<1:raise ValueError("capacity must be positive")
        self.capacity=capacity;self._items=deque(maxlen=capacity)
    def add(self,item):self._items.append(item)
    def sample(self,limit:int):return tuple(list(self._items)[-max(0,limit):])
    def __len__(self):return len(self._items)
