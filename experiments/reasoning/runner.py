from gene.world.inference import WorldReasoner
def infer(world,subject,name): return WorldReasoner(world).infer_property(subject,name)
