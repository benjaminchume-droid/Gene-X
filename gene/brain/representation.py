"""Structured-to-vector representation without requiring tokenization."""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import blake2b
from typing import Any, Iterable


@dataclass(frozen=True)
class FeatureVector:
    """Sparse feature vector used by the learned component."""

    values: dict[int, float]

    def items(self):
        return self.values.items()


@dataclass(frozen=True)
class StructuredExample:
    """A training/inference example expressed as structure rather than text tokens."""

    concepts: tuple[str, ...] = ()
    relations: tuple[tuple[str, str, str], ...] = ()
    properties: tuple[tuple[str, str, Any], ...] = ()
    state: tuple[tuple[str, Any], ...] = ()
    context: tuple[str, ...] = ()


def _feature_id(name: str, dimensions: int) -> int:
    digest = blake2b(name.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "little") % dimensions


def encode_structure(example: StructuredExample, dimensions: int = 4096) -> FeatureVector:
    """Encode meaning-bearing structure into sparse continuous features.

    This deliberately does not require a vocabulary or a fixed token sequence.
    Feature hashing is a compact interface to the trainable component; the
    underlying concepts and relations remain available outside the vector.
    """
    if dimensions < 64:
        raise ValueError("dimensions must be at least 64")
    out: dict[int, float] = {}

    def add(name: str, value: float = 1.0) -> None:
        i = _feature_id(name, dimensions)
        out[i] = out.get(i, 0.0) + value

    for concept in example.concepts:
        add("concept:" + concept)
    for relation, source, target in example.relations:
        add("relation:" + relation)
        add("relation:" + relation + ":source:" + source)
        add("relation:" + relation + ":target:" + target)
    for subject, key, value in example.properties:
        add("property:" + subject + ":" + key)
        add("property:" + subject + ":" + key + "=" + repr(value))
    for key, value in example.state:
        add("state:" + key)
        add("state:" + key + "=" + repr(value))
    for item in example.context:
        add("context:" + item)

    return FeatureVector(out)
