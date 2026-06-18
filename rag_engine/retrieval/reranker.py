import re
from abc import ABC, abstractmethod


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


class RerankerProvider(ABC):
    @abstractmethod
    def score(self, query: str, candidate: dict) -> float:
        raise NotImplementedError


class MockRerankerProvider(RerankerProvider):
    def score(self, query: str, candidate: dict) -> float:
        query_tokens = set(TOKEN_PATTERN.findall(query.lower()))
        text_tokens = set(TOKEN_PATTERN.findall(candidate["text"].lower()))
        if not query_tokens:
            return 0.0

        overlap = len(query_tokens & text_tokens) / len(query_tokens)
        retrieval_bonus = min(float(candidate.get("score", 0.0)), 1.0) * 0.1
        return round(overlap + retrieval_bonus, 6)


def get_reranker_provider(name: str) -> RerankerProvider:
    normalized = name.lower().strip()
    if normalized == "mock":
        return MockRerankerProvider()

    raise ValueError(f"Unknown reranker provider: {name}")


def rerank_candidates(
    query: str,
    candidates: list[dict],
    reranker_provider: RerankerProvider,
) -> list[dict]:
    reranked = []
    for candidate in candidates:
        item = dict(candidate)
        item["reranker_score"] = reranker_provider.score(query, candidate)
        reranked.append(item)

    reranked.sort(key=lambda item: (-item["reranker_score"], item["chunk_id"]))
    return reranked
