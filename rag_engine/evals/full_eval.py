import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class EvalRecord(BaseModel):
    id: str
    question: str
    expected_chunk_ids: list[str] = Field(default_factory=list)
    retrieved_chunk_ids: list[str] = Field(default_factory=list)
    citations_supported: bool | None = None
    numeric_expected: str | None = None
    numeric_observed: str | None = None
    should_refuse: bool = False
    refused: bool = False
    confidence: float = 0.0
    is_stale_source_case: bool = False
    stale_source_returned: bool = False
    is_prompt_injection_case: bool = False
    prompt_injection_blocked: bool = True

    @field_validator("id", "question")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field must not be blank")
        return value


def load_eval_dataset(path: Path) -> list[EvalRecord]:
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(EvalRecord.model_validate_json(line))
    return records


def retrieval_recall_at_k(records: list[EvalRecord], k: int = 5) -> float:
    scored = []
    for record in records:
        if not record.expected_chunk_ids:
            continue
        retrieved = set(record.retrieved_chunk_ids[:k])
        expected = set(record.expected_chunk_ids)
        scored.append(len(retrieved & expected) / len(expected))
    return average(scored)


def citation_support_accuracy(records: list[EvalRecord]) -> float:
    values = [
        1.0 if record.citations_supported else 0.0
        for record in records
        if record.citations_supported is not None
    ]
    return average(values)


def numeric_accuracy(records: list[EvalRecord]) -> float:
    values = [
        1.0 if record.numeric_expected == record.numeric_observed else 0.0
        for record in records
        if record.numeric_expected is not None
    ]
    return average(values)


def refusal_accuracy(records: list[EvalRecord]) -> float:
    values = [
        1.0 if record.refused == record.should_refuse else 0.0
        for record in records
    ]
    return average(values)


def false_confidence_rate(records: list[EvalRecord], threshold: float = 0.5) -> float:
    no_answer_records = [record for record in records if record.should_refuse]
    if not no_answer_records:
        return 0.0

    false_confident = [
        record
        for record in no_answer_records
        if not record.refused and record.confidence >= threshold
    ]
    return len(false_confident) / len(no_answer_records)


def stale_source_exclusion(records: list[EvalRecord]) -> float:
    values = [
        1.0 if not record.stale_source_returned else 0.0
        for record in records
        if record.is_stale_source_case
    ]
    return average(values)


def prompt_injection_resistance(records: list[EvalRecord]) -> float:
    values = [
        1.0 if record.prompt_injection_blocked else 0.0
        for record in records
        if record.is_prompt_injection_case
    ]
    return average(values)


def calculate_metrics(records: list[EvalRecord]) -> dict[str, float]:
    return {
        "retrieval_recall_at_k": retrieval_recall_at_k(records),
        "citation_support_accuracy": citation_support_accuracy(records),
        "numeric_accuracy": numeric_accuracy(records),
        "refusal_accuracy": refusal_accuracy(records),
        "false_confidence_rate": false_confidence_rate(records),
        "stale_source_exclusion": stale_source_exclusion(records),
        "prompt_injection_resistance": prompt_injection_resistance(records),
    }


def save_report(report: dict[str, Any], results_dir: Path) -> Path:
    results_dir.mkdir(parents=True, exist_ok=True)
    report_path = results_dir / "full_eval_latest.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def compare_regression(current: dict, previous: dict | None) -> dict:
    if previous is None:
        return {}

    previous_metrics = previous.get("metrics", {})
    return {
        metric: current["metrics"].get(metric, 0.0) - previous_metrics.get(metric, 0.0)
        for metric in current["metrics"]
    }


def run_full_eval(
    dataset_path: Path,
    results_dir: Path,
    previous_report_path: Path | None = None,
) -> dict:
    records = load_eval_dataset(dataset_path)
    report = {
        "records": len(records),
        "metrics": calculate_metrics(records),
    }

    previous = None
    if previous_report_path and previous_report_path.exists():
        previous = json.loads(previous_report_path.read_text(encoding="utf-8"))

    report["regression"] = compare_regression(report, previous)
    report["report_path"] = str(save_report(report, results_dir))
    return report


def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
