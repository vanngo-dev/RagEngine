# Phase 04 — Lightweight Eval and Debug Trace

## Video Goal

Make the query pipeline inspectable and persist lightweight eval results.

## Debug Endpoint Walkthrough

`POST /query/debug` runs the same retrieval and generation path as `/query`, but returns the intermediate trace used to produce the answer.

## Debug Fields

- `question`: the user question
- `vector_results`: ranked vector search output
- `selected_context`: source blocks selected for prompting
- `prompt_preview`: bounded prompt text for inspection
- `answer`: generated answer or refusal
- `citations`: citations extracted from the answer

## Eval Dataset Expansion

`data/evals/gold_lite.jsonl` now contains at least 10 lightweight questions so retrieval scoring has a broader starter set.

## Eval Result File Demo

Run:

```bash
python -m rag_engine.evals.lightweight_eval
```

The latest result is saved under:

```text
data/evals/results/lightweight_eval_latest.json
```

## Manual Demo

```bash
curl -X POST http://localhost:8000/query/debug \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What is this document about?\"}"
```

## Test Commands

```bash
pytest
```

## Validation Checklist

- `/query/debug` returns all required fields
- prompt preview is bounded
- eval dataset has at least 10 questions
- eval result file is created
- eval score is reproducible
- `/query` still works
