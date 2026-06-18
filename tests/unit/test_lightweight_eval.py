import json

from rag_engine.evals.lightweight_eval import run_lightweight_eval


def test_eval_score_is_reproducible_and_result_file_is_created(tmp_path) -> None:
    gold_path = tmp_path / "gold.jsonl"
    gold_path.write_text(
        json.dumps(
            {
                "id": "q-test",
                "question": "No matching chunk exists",
                "expected_chunk_ids": ["missing_chunk"],
                "top_k": 5,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    results_dir = tmp_path / "results"

    first = run_lightweight_eval(gold_path, results_dir)
    second = run_lightweight_eval(gold_path, results_dir)

    result_file = results_dir / "lightweight_eval_latest.json"
    assert first == second
    assert first["recall_at_k"] == 0.0
    assert result_file.exists()
    assert json.loads(result_file.read_text(encoding="utf-8")) == second
