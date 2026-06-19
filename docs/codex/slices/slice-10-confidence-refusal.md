# Slice 10 — Confidence and Refusal

## Goal

Add evidence-based confidence scoring and refusal behavior.

This slice makes the engine express uncertainty and refuse unsupported questions in a measurable way.

## Build Only This

- `ConfidenceScorer`
- refusal policy
- no-answer eval cases
- false-confidence metric
- confidence fields in `/query` response
- `docs/youtube/phase-10.md`

Do not build the full eval harness in this slice.

## Requirements

Use these positive confidence signals:

```text
direct evidence
verified citations
high reranker score
multiple agreeing sources
exact phrase match
```

Use these negative confidence signals:

```text
missing evidence
failed citation
unresolved conflict
weak retrieval
prompt-injection warning
```

Add these response fields:

```text
confidence
confidence_label
refusal
missing_information
```

Implementation requirements:

- Implement `ConfidenceScorer`.
- Implement a refusal policy driven by evidence and verification results.
- Add no-answer eval cases.
- Add a false-confidence metric.
- Lower confidence for failed citations.
- Lower confidence for unresolved conflicts.
- Lower confidence for weak retrieval.
- Lower confidence when prompt-injection warnings are present.
- Raise confidence for strong direct evidence with verified citations.
- Return missing information when refusing.
- Keep scoring deterministic and explainable in debug output.

## API Endpoints Required

Update:

```http
POST /query
POST /query/debug
```

`POST /query` response must include:

```text
confidence
confidence_label
refusal
missing_information
```

`POST /query/debug` must include the confidence signals used to score the response.

## Tests Required

Add tests for:

- strong evidence raises confidence
- weak evidence lowers confidence
- unsupported question refuses
- failed citation lowers confidence
- conflict lowers confidence
- prompt-injection warning lowers confidence

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Question not supported by the corpus\"}"

pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-10.md
```

The documentation must include:

- phase title: `Phase 10 — Confidence and Refusal`
- video goal
- confidence signal explanation
- refusal policy walkthrough
- no-answer case demo
- false-confidence metric explanation
- query response demo
- test commands
- validation checklist

## Acceptance Criteria

- `/query` includes confidence, confidence label, refusal, and missing information fields.
- Strong verified evidence raises confidence.
- Weak or missing evidence lowers confidence.
- Unsupported questions refuse.
- Failed citations lower confidence.
- Conflicts lower confidence.
- Prompt-injection warnings lower confidence.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 10.

Do not implement the full evaluation harness, regression reporting, production adapters, or UI.

Do not implement any future slice.
