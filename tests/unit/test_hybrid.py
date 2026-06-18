from rag_engine.retrieval.hybrid import reciprocal_rank_fusion


def result(chunk_id: str, score: float = 1.0) -> dict:
    return {
        "chunk_id": chunk_id,
        "document_id": "doc",
        "text": chunk_id,
        "score": score,
        "metadata": {"chunk_id": chunk_id},
    }


def test_rrf_output_deterministic_and_duplicates_merged() -> None:
    first = reciprocal_rank_fusion(
        {
            "keyword": [result("a"), result("b")],
            "vector": [result("a"), result("c")],
        }
    )
    second = reciprocal_rank_fusion(
        {
            "keyword": [result("a"), result("b")],
            "vector": [result("a"), result("c")],
        }
    )

    assert first == second
    assert [item["chunk_id"] for item in first] == ["a", "b", "c"]
    assert first[0]["ranking_signals"]["sources"] == ["keyword", "vector"]
