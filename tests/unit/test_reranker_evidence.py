from rag_engine.generation.evidence import EvidenceSelector
from rag_engine.retrieval.reranker import MockRerankerProvider, rerank_candidates


def candidate(chunk_id: str, text: str, section: str = "Risk") -> dict:
    return {
        "chunk_id": chunk_id,
        "document_id": "doc_1",
        "text": text,
        "score": 0.5,
        "metadata": {
            "section_title": section,
            "chunk_id": chunk_id,
            "document_id": "doc_1",
        },
    }


def test_reranker_scores_and_sorts_candidates() -> None:
    reranked = rerank_candidates(
        "supply chain risk",
        [
            candidate("weak", "unrelated text"),
            candidate("strong", "supply chain risk is tracked"),
        ],
        MockRerankerProvider(),
    )

    assert reranked[0]["chunk_id"] == "strong"
    assert reranked[0]["reranker_score"] > reranked[1]["reranker_score"]


def test_max_per_section_diversity_works() -> None:
    selected = EvidenceSelector(max_per_section=2).select(
        [
            candidate("c1", "supply chain risk one"),
            candidate("c2", "supply chain risk two"),
            candidate("c3", "supply chain risk three"),
        ]
    )

    total_selected = sum(len(items) for items in selected.values())
    assert total_selected == 2


def test_evidence_selector_classifies_and_flags_conflict() -> None:
    reranked = rerank_candidates(
        "risk",
        [
            candidate("primary", "risk is tracked"),
            candidate("conflict", "Conflict: this contradicts the prior source"),
            candidate("weak", "barely related", section="Other"),
        ],
        MockRerankerProvider(),
    )

    evidence = EvidenceSelector().select(reranked)

    assert evidence["primary_evidence"]
    assert evidence["weak_evidence"]
    assert evidence["conflicting_evidence"][0]["conflict_flag"] == "possible_conflict"
