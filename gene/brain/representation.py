"""Adaptive trainable representations for Gene X.

The representation layer is domain-neutral. It does not contain a vocabulary,
facts, object taxonomy, or task-specific rules. Features are discovered from
the structures supplied to it and their embeddings are learned from experience.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import blake2b
from math import sqrt, tanh
from random import Random
from typing import Any, Iterable


@dataclass(frozen=True)
class FeatureVector:
    values: dict[int, float]

    def items(self):
        return self.values.items()


@dataclass(frozen=True)
class StructuredExample:
    concepts: tuple[str, ...] = ()
    relations: tuple[tuple[str, str, str], ...] = ()
    properties: tuple[tuple[str, str, Any], ...] = ()
    state: tuple[tuple[str, Any], ...] = ()
    context: tuple[str, ...] = ()


@dataclass(frozen=True)
class Representation:
    values: tuple[float, ...]
    active_features: tuple[int, ...] = ()


@dataclass(frozen=True)
class RepresentationTrainingReport:
    steps: int
    mean_loss: float
    reconstruction_loss: float
    supervised_loss: float


def _feature_id(name: str, dimensions: int) -> int:
    digest = blake2b(name.encode("utf-8"), digest_size=8).digest()
    return int.from_bytes(digest, "little") % dimensions


def encode_structure(example: StructuredExample, dimensions: int = 8192) -> FeatureVector:
    if dimensions < 128:
        raise ValueError("dimensions must be at least 128")
    out: dict[int, float] = {}

    def add(name: str, value: float = 1.0) -> None:
        index = _feature_id(name, dimensions)
        out[index] = out.get(index, 0.0) + value

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


class TrainableRepresentation:
    """A compact learned representation with embeddings, encoder and decoder.

    It is intentionally smaller than a foundation model and has no fixed
    semantic dictionary. The feature table, encoder and decoder are all
    trainable. A task head can optionally be trained on top without making the
    representation itself depend on that task.
    """

    def __init__(
        self,
        *,
        input_size: int = 8192,
        embedding_size: int = 48,
        representation_size: int = 128,
        seed: int = 7,
    ) -> None:
        if input_size < 128 or embedding_size < 4 or representation_size < 8:
            raise ValueError("invalid representation dimensions")
        self.input_size = input_size
        self.embedding_size = embedding_size
        self.representation_size = representation_size
        self._rng = Random(seed)
        self.embeddings: dict[int, list[float]] = {}
        self.encoder = self._matrix(representation_size, embedding_size)
        self.decoder = self._matrix(embedding_size, representation_size)
        self.encoder_bias = [0.0] * representation_size
        self.decoder_bias = [0.0] * embedding_size
        self.training_steps = 0

    def _matrix(self, rows: int, cols: int) -> list[list[float]]:
        scale = 1.0 / sqrt(max(1, cols))
        return [[self._rng.uniform(-scale, scale) for _ in range(cols)] for _ in range(rows)]

    def _embedding(self, index: int) -> list[float]:
        vector = self.embeddings.get(index)
        if vector is None:
            scale = 1.0 / sqrt(self.embedding_size)
            vector = [self._rng.uniform(-scale, scale) for _ in range(self.embedding_size)]
            self.embeddings[index] = vector
        return vector

    def _pooled(self, features: FeatureVector) -> list[float]:
        pooled = [0.0] * self.embedding_size
        norm = 0.0
        for index, weight in features.items():
            vector = self._embedding(index)
            norm += abs(weight)
            for j, value in enumerate(vector):
                pooled[j] += value * weight
        if norm:
            pooled = [value / norm for value in pooled]
        return pooled

    def encode(self, example: StructuredExample | FeatureVector) -> Representation:
        features = example if isinstance(example, FeatureVector) else encode_structure(example, self.input_size)
        pooled = self._pooled(features)
        values = []
        for row, bias in zip(self.encoder, self.encoder_bias):
            values.append(tanh(sum(w * x for w, x in zip(row, pooled)) + bias))
        return Representation(tuple(values), tuple(features.values))

    def _reconstruct(self, representation: Representation) -> list[float]:
        return [
            tanh(sum(w * x for w, x in zip(row, representation.values)) + bias)
            for row, bias in zip(self.decoder, self.decoder_bias)
        ]

    def train_autoencoding(
        self,
        examples: Iterable[StructuredExample],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ) -> RepresentationTrainingReport:
        batch = [encode_structure(item, self.input_size) for item in examples]
        if not batch:
            return RepresentationTrainingReport(0, 0.0, 0.0, 0.0)
        if epochs < 1 or learning_rate <= 0:
            raise ValueError("epochs must be positive and learning_rate must be positive")

        total_loss = 0.0
        steps = 0
        for _ in range(epochs):
            for features in batch:
                pooled = self._pooled(features)
                representation = self.encode(features)
                reconstruction = self._reconstruct(representation)
                target = [0.0] * self.embedding_size
                for index, weight in features.items():
                    vector = self._embedding(index)
                    for j, value in enumerate(vector):
                        target[j] += value * weight
                norm = sum(abs(v) for v in target)
                if norm:
                    target = [v / norm for v in target]

                grad_decoder = [0.0] * self.embedding_size
                grad_rep = [0.0] * self.representation_size
                loss = 0.0
                for j, (pred, truth) in enumerate(zip(reconstruction, target)):
                    error = pred - truth
                    loss += error * error
                    grad = 2.0 * error * (1.0 - pred * pred)
                    grad_decoder[j] = grad
                    for k in range(self.representation_size):
                        grad_rep[k] += grad * self.decoder[j][k]
                        self.decoder[j][k] -= learning_rate * grad * representation.values[k]
                    self.decoder_bias[j] -= learning_rate * grad

                for k, grad in enumerate(grad_rep):
                    dz = grad * (1.0 - representation.values[k] ** 2)
                    self.encoder_bias[k] -= learning_rate * dz
                    for j in range(self.embedding_size):
                        self.encoder[k][j] -= learning_rate * dz * pooled[j]

                # The feature embeddings are updated through the encoder path.
                grad_pooled = [0.0] * self.embedding_size
                for k, grad in enumerate(grad_rep):
                    dz = grad * (1.0 - representation.values[k] ** 2)
                    for j in range(self.embedding_size):
                        grad_pooled[j] += dz * self.encoder[k][j]
                count = max(1, len(features.values))
                for index, weight in features.items():
                    vector = self._embedding(index)
                    scale = learning_rate * weight / count
                    for j in range(self.embedding_size):
                        vector[j] -= scale * grad_pooled[j]

                total_loss += loss / self.embedding_size
                steps += 1
                self.training_steps += 1

        mean = total_loss / max(1, steps)
        return RepresentationTrainingReport(steps, mean, mean, 0.0)

    def train_pairs(
        self,
        pairs: Iterable[tuple[StructuredExample, StructuredExample, float]],
        *,
        epochs: int = 1,
        learning_rate: float = 0.01,
    ) -> RepresentationTrainingReport:
        """Learn relational geometry from pairs without requiring class labels.

        target_similarity is expected in [0, 1]. Similar examples are pulled
        together and dissimilar examples are pushed apart by a margin loss.
        """
        batch = list(pairs)
        if not batch:
            return RepresentationTrainingReport(0, 0.0, 0.0, 0.0)
        total = 0.0
        steps = 0
        for _ in range(epochs):
            for left, right, target in batch:
                if not 0.0 <= target <= 1.0:
                    raise ValueError("target similarity must be between 0 and 1")
                a = self.encode(left)
                b = self.encode(right)
                distance = sqrt(sum((x - y) ** 2 for x, y in zip(a.values, b.values)) + 1e-9)
                desired = 1.0 - target
                margin = 1.0
                if target > 0.5:
                    loss = distance * distance
                    scale = 2.0
                else:
                    gap = max(0.0, margin - distance)
                    loss = gap * gap
                    scale = -2.0 * gap / max(distance, 1e-6)
                if target > 0.5:
                    scale = 2.0 / max(1.0, distance)
                # Update only the persistent embedding table. This keeps the
                # operation stable and makes the learned geometry reusable.
                for feature_set, sign in ((left, 1.0), (right, -1.0)):
                    encoded = encode_structure(feature_set, self.input_size)
                    for index, weight in encoded.items():
                        vector = self._embedding(index)
                        direction = [(x - y) for x, y in zip(a.values, b.values)]
                        magnitude = sum(direction) or 1.0
                        step = learning_rate * scale * sign * weight / magnitude
                        for j in range(self.embedding_size):
                            vector[j] -= step * (direction[j % self.representation_size])
                total += loss + desired * 0.0
                steps += 1
                self.training_steps += 1
        mean = total / max(1, steps)
        return RepresentationTrainingReport(steps, mean, 0.0, mean)

    def state_dict(self) -> dict[str, Any]:
        return {
            "input_size": self.input_size,
            "embedding_size": self.embedding_size,
            "representation_size": self.representation_size,
            "embeddings": {str(k): v[:] for k, v in self.embeddings.items()},
            "encoder": [row[:] for row in self.encoder],
            "decoder": [row[:] for row in self.decoder],
            "encoder_bias": self.encoder_bias[:],
            "decoder_bias": self.decoder_bias[:],
            "training_steps": self.training_steps,
        }

    @classmethod
    def from_state_dict(cls, state: dict[str, Any]) -> "TrainableRepresentation":
        obj = cls(
            input_size=int(state["input_size"]),
            embedding_size=int(state["embedding_size"]),
            representation_size=int(state["representation_size"]),
        )
        obj.embeddings = {int(k): list(v) for k, v in state["embeddings"].items()}
        obj.encoder = [list(row) for row in state["encoder"]]
        obj.decoder = [list(row) for row in state["decoder"]]
        obj.encoder_bias = list(state["encoder_bias"])
        obj.decoder_bias = list(state["decoder_bias"])
        obj.training_steps = int(state.get("training_steps", 0))
        return obj
