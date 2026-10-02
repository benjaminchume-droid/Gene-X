from trainers.curriculum.engine import Lesson
import json
from pathlib import Path
def load(path)->tuple[Lesson,...]:
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(Lesson(x["lesson_id"],x.get("payload"),tuple(x.get("prerequisites",()))) for x in data)
