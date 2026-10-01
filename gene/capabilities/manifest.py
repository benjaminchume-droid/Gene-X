"""Export capability metadata to orchestrators and external interfaces."""
class CapabilityManifest:
 def __init__(self,capabilities,skills=None):self.capabilities=capabilities;self.skills=skills
 def export(self):
  return {"capabilities":[{"name":c.name,"description":c.description,"source":c.source,"permissions":sorted(c.permissions),"input_schema":c.input_schema,"output_schema":c.output_schema} for c in self.capabilities.find()],"skills":[{"name":s.name,"purpose":s.purpose,"success_rate":s.success_rate} for s in self.skills._skills.values()] if self.skills else []}
