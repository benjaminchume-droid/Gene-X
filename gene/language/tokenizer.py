"""Optional lexical adapter. Tokenization is an I/O mechanism, not Gene's thought substrate."""
from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Token:
    text: str
    start: int
    end: int
    kind: str = "word"

class Tokenizer:
    _pattern = re.compile(r"\\w+|[^\\w\\s]", re.UNICODE)
    def tokenize(self, text: str) -> list[Token]:
        return [Token(m.group(0), m.start(), m.end(), "word" if m.group(0).isalnum() else "punctuation") for m in self._pattern.finditer(text)]
