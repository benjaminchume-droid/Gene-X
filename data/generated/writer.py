from data.records import write_jsonl
from data.schemas.records import Record
def write(records,path): write_jsonl((r if isinstance(r,Record) else Record(str(i),r) for i,r in enumerate(records)),path)
