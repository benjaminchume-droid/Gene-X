"""Compression boundary for representations that benefit from compact storage."""
from __future__ import annotations
from typing import Any, Protocol

class Codec(Protocol):
    def encode(self, value: Any) -> bytes: ...
    def decode(self, payload: bytes) -> Any: ...

class Compressor:
    def __init__(self, codec: Codec) -> None:
        self.codec = codec

    def compress(self, value: Any) -> bytes:
        return self.codec.encode(value)

    def decompress(self, payload: bytes) -> Any:
        return self.codec.decode(payload)
