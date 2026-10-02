from gene.memory.retrieval import MemoryRetriever
def retrieve(store,encoder,value,limit=8): return MemoryRetriever(store,encoder).query(value,limit=limit)
