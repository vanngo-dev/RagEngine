import json
from pathlib import Path

from app.config import get_settings
from rag_engine.retrieval.embeddings import get_embedding_provider
from rag_engine.retrieval.vector_index import SQLiteVectorIndex


DEFAULT_GOLD_PATH = Path("data/evals/gold_lite.jsonl")


def recall_at_k(retrieved_ids: list[str], expected_ids: list[str], k: int) -> float:
    if not expected_ids:
        return 0.0

    retrieved_top_k = set(retrieved_ids[:k])
    expected = set(expected_ids)
    return len(retrieved_top_k & expected) / len(expected)


def load_gold_records(path: Path = DEFAULT_GOLD_PATH) -> list[dict]:
    if not path.exists():
        return []

    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))

    return records


def run_lightweight_eval(gold_path: Path = DEFAULT_GOLD_PATH) -> dict:
    settings = get_settings()
    provider = get_embedding_provider(settings.embedding_provider)
    vector_index = SQLiteVectorIndex(settings.database_path)
    records = load_gold_records(gold_path)

    scores = []
    for record in records:
        top_k = int(record.get("top_k", 5))
        query_vector = provider.embed_text(record["question"])
        results = vector_index.search(query_vector, top_k=top_k)
        retrieved_ids = [result["chunk_id"] for result in results]
        expected_ids = record.get("expected_chunk_ids", [])
        scores.append(recall_at_k(retrieved_ids, expected_ids, top_k))

    recall = sum(scores) / len(scores) if scores else 0.0
    return {
        "records": len(records),
        "metric": "recall_at_k",
        "recall_at_k": recall,
    }


def main() -> None:
    print(json.dumps(run_lightweight_eval(), indent=2))


if __name__ == "__main__":
    main()
