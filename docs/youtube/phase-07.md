# Phase 07 — Reranker and Evidence Selector

## Video Goal

Rerank hybrid retrieval candidates, apply diversity limits, classify evidence, and expose the evidence trace in `/query/debug`.

## Reranker Provider

The reranking layer now has a `RerankerProvider` interface and deterministic `MockRerankerProvider` for tests. The mock scores candidates by query-token overlap with a small retrieval-score bonus.

## Rerank Pipeline

The query debug path now runs hybrid retrieval, reranks candidates, and passes selected evidence into the context builder.

## Diversity Control

Evidence selection limits results to a maximum of two chunks per document section by default. This prevents a single section from crowding out other useful evidence.

## Evidence Categories

Selected evidence is classified into:

- `primary_evidence`
- `supporting_evidence`
- `weak_evidence`
- `conflicting_evidence`

## Conflict Flag Demo

Simple conflict flags are raised for fixture-style phrases such as `Conflict:` or `contradicts`.

## Debug Trace Demo

```bash
curl -X POST http://localhost:8000/query/debug \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What does the document say?\"}"
```

The response includes rerank results and selected evidence.

## Test Commands

```bash
pytest
```

## Validation Checklist

- reranker scores candidates
- candidates are sorted by reranker score
- diversity limits max chunks per section
- evidence categories are populated
- conflict flags appear for conflict fixtures
- `/query/debug` includes rerank and selected evidence output
