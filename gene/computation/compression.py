"""Compression interface for compact representations."""
from __future__ import annotations
from typing import Any, Callable

class Compressor:
    def __init__(self, encode: Callable[[Any], Any], decode: Callable[[Any], Any]) -> None:
        self.encode = encode
        self.decode = decode

    def compress(self, value: Any) -> Any:
        return self.encode(value)

    def decompress(self, value: Any) -> Any:
        return self.decode(value)
