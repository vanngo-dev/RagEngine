import json

import pytest
from pydantic import ValidationError

from rag_engine.evals.full_eval import (
    EvalRecord,
    calculate_metrics,
    load_eval_dataset,
    prompt_injection_resistance,
    run_full_eval,
    stale_source_exclusion,
)


def records() -> list[EvalRecord]:
    return [
        EvalRecord(
            id="retrieval",
            question="q",
            expected_chunk_ids=["a"],
            retrieved_chunk_ids=["a", "b"],
            citations_supported=True,
            should_refuse=False,
            refused=False,
            confidence=0.8,
        ),
        EvalRecord(
            id="numeric",
            question="q",
            numeric_expected="42",
            numeric_observed="42",
            should_refuse=False,
            refused=False,
        ),
        EvalRecord(
            id="refusal",
            question="q",
            should_refuse=True,
            refused=True,
            confidence=0.1,
        ),
        EvalRecord(
            id="false-confidence",
            question="q",
            should_refuse=True,
            refused=False,
            confidence=0.9,
        ),
        EvalRecord(
            id="stale",
            question="q",
            is_stale_source_case=True,
            stale_source_returned=False,
        ),
        EvalRecord(
            id="injection",
            question="q",
            is_prompt_injection_case=True,
            prompt_injection_blocked=True,
        ),
    ]


def test_eval_dataset_validates(tmp_path) -> None:
    path = tmp_path / "full_eval.jsonl"
    path.write_text(
        json.dumps({"id": "case-1", "question": "Valid question?"}) + "\n",
        encoding="utf-8",
    )

    loaded = load_eval_dataset(path)

    assert loaded[0].id == "case-1"


def test_eval_dataset_rejects_blank_id() -> None:
    with pytest.raises(ValidationError):
        EvalRecord(id="", question="Valid question?")


def test_each_metric_calculation_is_tested() -> None:
    metrics = calculate_metrics(records())

    assert metrics["retrieval_recall_at_k"] == 1.0
    assert metrics["citation_support_accuracy"] == 1.0
    assert metrics["numeric_accuracy"] == 1.0
    assert metrics["refusal_accuracy"] == 5 / 6
    assert metrics["false_confidence_rate"] == 0.5
    assert metrics["stale_source_exclusion"] == 1.0
    assert metrics["prompt_injection_resistance"] == 1.0


def test_report_is_saved_with_regression_support(tmp_path) -> None:
    dataset = tmp_path / "full_eval.jsonl"
    dataset.write_text(
        json.dumps(
            {
                "id": "case",
                "question": "q",
                "expected_chunk_ids": ["a"],
                "retrieved_chunk_ids": ["a"],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    previous = tmp_path / "previous.json"
    previous.write_text(
        json.dumps({"metrics": {"retrieval_recall_at_k": 0.5}}),
        encoding="utf-8",
    )

    report = run_full_eval(dataset, tmp_path / "results", previous)

    assert (tmp_path / "results" / "full_eval_latest.json").exists()
    assert report["regression"]["retrieval_recall_at_k"] == 0.5


def test_stale_source_and_prompt_injection_eval_work() -> None:
    assert stale_source_exclusion(records()) == 1.0
    assert prompt_injection_resistance(records()) == 1.0
