import math
import re
from abc import ABC, abstractmethod


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_text(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]


class FakeEmbeddingProvider(EmbeddingProvider):
    def __init__(self, dimensions: int = 64) -> None:
        self.dimensions = dimensions

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        tokens = TOKEN_PATTERN.findall(text.lower())

        for token in tokens:
            index = sum(ord(character) for character in token) % self.dimensions
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0:
            return vector

        return [value / norm for value in vector]


class LocalEmbeddingProvider(EmbeddingProvider):
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError(
            "LocalEmbeddingProvider is a placeholder. Configure a concrete local embedding backend before selecting it."
        )


def get_embedding_provider(name: str) -> EmbeddingProvider:
    normalized = name.lower().strip()
    if normalized in {"fake", "deterministic_fake"}:
        return FakeEmbeddingProvider()
    if normalized in {"local", "local_placeholder"}:
        return LocalEmbeddingProvider()

    raise ValueError(f"Unknown embedding provider: {name}")
