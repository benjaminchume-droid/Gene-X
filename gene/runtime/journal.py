"""Durable append-only runtime journal.

The journal records state transitions and observations without prescribing domain
semantics. It is intentionally small so a durable backend can replace it.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable

@dataclass(frozen=True, slots=True)
class JournalEntry:
    sequence: int
    event: str
    payload: dict[str, Any]

class RuntimeJournal:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path is not None else None
        self._entries: list[JournalEntry] = []
        if self.path is not None and self.path.exists():
            self._load()

    def append(self, event: str, payload: dict[str, Any] | None = None) -> JournalEntry:
        entry = JournalEntry(len(self._entries) + 1, event, dict(payload or {}))
        self._entries.append(entry)
        if self.path is not None:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(asdict(entry), default=str, sort_keys=True) + "\n")
                handle.flush()
        return entry

    def entries(self) -> tuple[JournalEntry, ...]:
        return tuple(self._entries)

    def replay(self, events: Iterable[JournalEntry] | None = None) -> tuple[JournalEntry, ...]:
        return tuple(self._entries if events is None else events)

    def _load(self) -> None:
        self._entries.clear()
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            self._entries.append(JournalEntry(int(item["sequence"]), str(item["event"]), dict(item["payload"])))
