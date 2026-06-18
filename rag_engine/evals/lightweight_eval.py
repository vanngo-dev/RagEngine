import json
from pathlib import Path

from app.config import get_settings
from rag_engine.retrieval.embeddings import get_embedding_provider
from rag_engine.retrieval.hybrid import hybrid_search
from rag_engine.retrieval.keyword_index import SQLiteKeywordIndex
from rag_engine.retrieval.vector_index import SQLiteVectorIndex


DEFAULT_GOLD_PATH = Path("data/evals/gold_lite.jsonl")
DEFAULT_RESULTS_DIR = Path("data/evals/results")
DEFAULT_RESULT_FILE = "lightweight_eval_latest.json"


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


def run_lightweight_eval(
    gold_path: Path = DEFAULT_GOLD_PATH,
    results_dir: Path = DEFAULT_RESULTS_DIR,
    save_result: bool = True,
) -> dict:
    settings = get_settings()
    provider = get_embedding_provider(settings.embedding_provider)
    vector_index = SQLiteVectorIndex(settings.database_path)
    keyword_index = SQLiteKeywordIndex(settings.database_path)
    records = load_gold_records(gold_path)

    vector_scores = []
    keyword_scores = []
    hybrid_scores = []
    for record in records:
        top_k = int(record.get("top_k", 5))
        query_vector = provider.embed_text(record["question"])
        vector_results = vector_index.search(query_vector, top_k=top_k)
        keyword_results = keyword_index.search(record["question"], top_k=top_k)
        hybrid_results = hybrid_search(
            query=record["question"],
            top_k=top_k,
            vector_index=vector_index,
            keyword_index=keyword_index,
            embedding_provider=provider,
        )
        expected_ids = record.get("expected_chunk_ids", [])
        vector_scores.append(
            recall_at_k([result["chunk_id"] for result in vector_results], expected_ids, top_k)
        )
        keyword_scores.append(
            recall_at_k([result["chunk_id"] for result in keyword_results], expected_ids, top_k)
        )
        hybrid_scores.append(
            recall_at_k([result["chunk_id"] for result in hybrid_results], expected_ids, top_k)
        )

    vector_recall = average(vector_scores)
    keyword_recall = average(keyword_scores)
    hybrid_recall = average(hybrid_scores)
    result = {
        "records": len(records),
        "metric": "recall_at_k",
        "recall_at_k": vector_recall,
        "vector_recall_at_k": vector_recall,
        "keyword_recall_at_k": keyword_recall,
        "hybrid_recall_at_k": hybrid_recall,
    }

    if save_result:
        save_eval_result(result, results_dir)

    return result


def save_eval_result(result: dict, results_dir: Path = DEFAULT_RESULTS_DIR) -> Path:
    results_dir.mkdir(parents=True, exist_ok=True)
    result_path = results_dir / DEFAULT_RESULT_FILE
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result_path


def average(scores: list[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0


def main() -> None:
    print(json.dumps(run_lightweight_eval(), indent=2))


if __name__ == "__main__":
    main()
