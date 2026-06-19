# Slice 11 — Full Evaluation Harness

## Goal

Add full eval for retrieval, citations, refusal, numeric accuracy, stale-source exclusion, and prompt-injection resistance.

This slice creates a broader regression-oriented evaluation harness for the engine.

## Build Only This

- expanded eval dataset schema
- full eval runner
- JSON report output
- regression report support
- metric calculation tests
- `docs/youtube/phase-11.md`

Do not build production adapters in this slice.

## Requirements

Implement these metrics:

```text
retrieval_recall_at_k
citation_support_accuracy
numeric_accuracy
refusal_accuracy
false_confidence_rate
stale_source_exclusion
prompt_injection_resistance
```

Required CLI:

```bash
python -m rag_engine.evals.run_full_eval
```

Implementation requirements:

- Define an expanded eval dataset schema.
- Validate eval dataset records before running.
- Implement a full eval runner.
- Save JSON reports to a stable results directory.
- Support regression report comparison against a previous report.
- Keep metric calculations isolated and unit tested.
- Include stale-source exclusion cases.
- Include prompt-injection resistance cases.
- Include numeric accuracy cases.
- Include refusal/no-answer cases.
- Preserve the lightweight eval CLI from earlier slices.

## API Endpoints Required

No new HTTP endpoints are required.

The eval runner may call existing application services or test clients, but this slice is focused on CLI and report behavior.

## Tests Required

Add tests for:

- eval dataset validates
- each metric calculation is tested
- report is saved
- stale-source test works
- prompt-injection eval works

## Manual Validation

Run:

```bash
python -m rag_engine.evals.run_full_eval
pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-11.md
```

The documentation must include:

- phase title: `Phase 11 — Full Evaluation Harness`
- video goal
- eval dataset schema explanation
- metric overview
- full eval runner demo
- JSON report output demo
- regression report explanation
- test commands
- validation checklist

## Acceptance Criteria

- `python -m rag_engine.evals.run_full_eval` runs successfully.
- Dataset records are validated.
- All required metrics are calculated.
- JSON reports are saved.
- Regression report support exists.
- Stale-source exclusion is evaluated.
- Prompt-injection resistance is evaluated.
- Metric calculation tests pass.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 11.

Do not implement production adapter interfaces, PostgreSQL, Qdrant, OpenSearch, Redis, deployment logic, or UI.

Do not implement any future slice.
