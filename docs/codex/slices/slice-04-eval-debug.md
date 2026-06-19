# Slice 04 — Lightweight Eval and Debug Trace

## Goal

Add `/query/debug` and improve lightweight evaluation.

This slice makes the query pipeline inspectable and makes the lightweight eval more useful while keeping it deterministic.

## Build Only This

- `POST /query/debug`
- query trace output
- expanded `gold_lite.jsonl`
- eval result file output
- `docs/youtube/phase-04.md`

Do not build hybrid retrieval or reranking in this slice.

## Requirements

The debug response must include:

```text
question
vector_results
selected_context
prompt_preview
answer
citations
```

Implementation requirements:

- Expand `data/evals/gold_lite.jsonl` to at least 10 questions.
- Store eval results under:

```text
data/evals/results/
```

- Keep eval behavior simple and deterministic.
- Keep `/query` behavior stable while adding `/query/debug`.
- Use mocked LLM behavior in tests.
- Avoid exposing secrets or environment values in debug output.
- Ensure `prompt_preview` is useful but bounded in size.

## API Endpoints Required

Implement:

```http
POST /query/debug
```

Request body:

```json
{
  "question": "What is this document about?"
}
```

The response must include all required debug fields.

## Tests Required

Add tests for:

- debug output includes required fields
- eval score is reproducible
- eval result file is created
- debug endpoint works with mocked LLM

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/query/debug \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is this document about?\"}"

python -m rag_engine.evals.lightweight_eval
pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-04.md
```

The documentation must include:

- phase title: `Phase 04 — Lightweight Eval and Debug Trace`
- video goal
- debug endpoint walkthrough
- explanation of every debug field
- eval dataset expansion overview
- eval result file demo
- test commands
- validation checklist

## Acceptance Criteria

- `/query/debug` returns the required trace fields.
- The lightweight eval dataset contains at least 10 questions.
- Eval results are written under `data/evals/results/`.
- Eval scores are reproducible.
- `/query` still works.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 04.

Do not implement hybrid retrieval, keyword search, Reciprocal Rank Fusion, reranking, evidence selection, citation verification, confidence scoring, full evaluation, production adapters, or UI.

Do not implement any future slice.
