# Slice 07 — Reranker and Evidence Selector

## Goal

Add reranking, diversity control, and evidence selection.

This slice improves the quality and structure of evidence passed into answer generation.

## Build Only This

- `RerankerProvider` interface
- `MockRerankerProvider` for tests
- rerank pipeline after hybrid retrieval
- diversity control
- `EvidenceSelector`
- simple conflict flags
- `docs/youtube/phase-07.md`

Do not build prompt-injection defense or citation verification in this slice.

## Requirements

Apply reranking after hybrid retrieval.

Diversity control:

```text
max 2 chunks per document section by default
```

Evidence categories:

```text
primary_evidence
supporting_evidence
weak_evidence
conflicting_evidence
```

Implementation requirements:

- Add a reranker provider interface.
- Add a mock reranker provider for deterministic tests.
- Rerank hybrid candidates before evidence selection.
- Sort reranked candidates by reranker score.
- Apply max-per-section diversity control.
- Implement `EvidenceSelector`.
- Classify selected evidence into the required categories.
- Add simple conflict flags for obvious fixture-based conflicts.
- Extend `/query/debug` to include rerank and selected evidence output.
- Preserve existing `/query` behavior while improving evidence selection.

## API Endpoints Required

No brand-new HTTP endpoint is required.

Update:

```http
POST /query/debug
```

The debug response must include rerank details and selected evidence output.

The query pipeline may also use reranked selected evidence for:

```http
POST /query
```

## Tests Required

Add tests for:

- reranker scores candidates
- reranked candidates are sorted
- max-per-section diversity works
- evidence selector classifies evidence
- conflict flag appears for test fixture
- `/query/debug` includes rerank and selected evidence output

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/query/debug \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What does the document say?\"}"

pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-07.md
```

The documentation must include:

- phase title: `Phase 07 — Reranker and Evidence Selector`
- video goal
- reranker provider explanation
- rerank pipeline walkthrough
- diversity control explanation
- evidence category explanation
- conflict flag demo
- debug trace demo
- test commands
- validation checklist

## Acceptance Criteria

- Hybrid candidates can be reranked.
- Mock reranker produces deterministic scores.
- Reranked candidates are sorted by score.
- Diversity control limits chunks per document section.
- Evidence is classified into the required categories.
- `/query/debug` shows reranking and selected evidence.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 07.

Do not implement prompt-injection defense, structured claims, citation verification, confidence scoring, full evaluation, production adapters, or UI.

Do not implement any future slice.
