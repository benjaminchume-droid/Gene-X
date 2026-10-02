import json
from pathlib import Path
from typing import Iterable
from data.schemas.records import Record
def write_jsonl(records:Iterable[Record],path)->None:
    with Path(path).open("w",encoding="utf-8") as h:
        for record in records: h.write(json.dumps(record.to_dict(),ensure_ascii=False)+"\n")
def read_jsonl(path)->tuple[Record,...]:
    out=[]
    with Path(path).open("r",encoding="utf-8") as h:
        for line in h:
            if line.strip():
                x=json.loads(line); out.append(Record(x["record_id"],x.get("input"),x.get("target"),dict(x.get("metadata",{}))))
    return tuple(out)
