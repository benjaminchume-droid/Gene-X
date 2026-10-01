"""Discoverable capability registry."""
class CapabilityRegistry:
 def __init__(self):self._items={}
 def register(self,c):
  if c.name in self._items:raise ValueError(f"capability already registered: {c.name}")
  self._items[c.name]=c
 def replace(self,c):self._items[c.name]=c
 def get(self,name):return self._items[name]
 def find(self,*,names=None,permissions=None,source=None):
  xs=list(self._items.values())
  if names is not None:xs=[c for c in xs if c.name in names]
  if permissions is not None:xs=[c for c in xs if set(permissions).issubset(c.permissions)]
  if source is not None:xs=[c for c in xs if c.source==source]
  return xs
 def names(self):return sorted(self._items)
