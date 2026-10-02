import sqlite3
from dataclasses import dataclass
@dataclass
class DatabaseTool:
    path:str=":memory:"
    def connect(self):return sqlite3.connect(self.path)
    def execute(self,sql:str,params=()):
        with self.connect() as db:
            cur=db.execute(sql,params); rows=cur.fetchall(); db.commit(); return rows
