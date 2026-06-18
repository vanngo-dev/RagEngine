# Phase 11 — Full Evaluation Harness

## Video Goal

Add a full JSON-reporting eval harness for retrieval, citations, refusal, numeric accuracy, stale-source exclusion, and prompt-injection resistance.

## Eval Dataset Schema

Each JSONL record validates fields such as:

- `id`
- `question`
- `expected_chunk_ids`
- `retrieved_chunk_ids`
- `citations_supported`
- `numeric_expected`
- `numeric_observed`
- `should_refuse`
- `refused`
- `confidence`
- stale-source and prompt-injection flags

## Metric Overview

The harness calculates:

- `retrieval_recall_at_k`
- `citation_support_accuracy`
- `numeric_accuracy`
- `refusal_accuracy`
- `false_confidence_rate`
- `stale_source_exclusion`
- `prompt_injection_resistance`

## Full Eval Runner Demo

```bash
python -m rag_engine.evals.run_full_eval
```

## JSON Report Output

Reports are saved to:

```text
data/evals/results/full_eval_latest.json
```

## Regression Report

Pass `--previous-report` to compare current metrics against an earlier JSON report. The output includes metric deltas under `regression`.

## Test Commands

```bash
pytest
```

## Validation Checklist

- dataset records validate
- each metric has unit tests
- report is saved
- regression comparison works
- stale-source cases are evaluated
- prompt-injection cases are evaluated
