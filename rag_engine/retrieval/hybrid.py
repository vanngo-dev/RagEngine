from rag_engine.retrieval.embeddings import EmbeddingProvider
from rag_engine.retrieval.keyword_index import SQLiteKeywordIndex
from rag_engine.retrieval.vector_index import SQLiteVectorIndex


def reciprocal_rank_fusion(
    result_sets: dict[str, list[dict]],
    rrf_k: int = 60,
) -> list[dict]:
    merged: dict[str, dict] = {}

    for source_name in sorted(result_sets):
        for rank, result in enumerate(result_sets[source_name], start=1):
            chunk_id = result["chunk_id"]
            if chunk_id not in merged:
                candidate = dict(result)
                candidate["ranking_signals"] = {
                    "rrf_score": 0.0,
                    "sources": [],
                    "ranks": {},
                    "scores": {},
                }
                merged[chunk_id] = candidate

            candidate = merged[chunk_id]
            candidate["ranking_signals"]["rrf_score"] += 1.0 / (rrf_k + rank)
            candidate["ranking_signals"]["sources"].append(source_name)
            candidate["ranking_signals"]["ranks"][source_name] = rank
            candidate["ranking_signals"]["scores"][source_name] = result["score"]

    fused = list(merged.values())
    for candidate in fused:
        candidate["ranking_signals"]["sources"].sort()

    fused.sort(
        key=lambda candidate: (
            -candidate["ranking_signals"]["rrf_score"],
            candidate["chunk_id"],
        )
    )
    return fused


def hybrid_search(
    query: str,
    top_k: int,
    vector_index: SQLiteVectorIndex,
    keyword_index: SQLiteKeywordIndex,
    embedding_provider: EmbeddingProvider,
    include_superseded: bool = False,
    filters: dict[str, str] | None = None,
) -> list[dict]:
    filters = filters or {}
    keyword_results = keyword_index.search(
        query,
        top_k=50,
        include_superseded=include_superseded,
        filters=filters,
    )
    query_vector = embedding_provider.embed_text(query)
    vector_results = vector_index.search(
        query_vector,
        top_k=50,
        include_superseded=include_superseded,
        filters=filters,
    )

    return reciprocal_rank_fusion(
        {
            "keyword": keyword_results,
            "vector": vector_results,
        }
    )[:top_k]
