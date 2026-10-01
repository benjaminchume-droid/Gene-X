"""Discoverable skill registry with no hard-coded task catalogue."""
from .skills import Skill
class SkillRegistry:
 def __init__(self):self._skills={}
 def register(self,skill):
  if skill.name in self._skills:raise ValueError(f"skill already registered: {skill.name}")
  self._skills[skill.name]=skill
 def get(self,name):return self._skills[name]
 def applicable(self,state):return [s for s in self._skills.values() if s.applicable(state)]
 def names(self):return sorted(self._skills)
