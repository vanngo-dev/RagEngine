# Slice 09 — Structured Claims and Citation Verification

## Goal

Generate structured claims and verify citations.

This slice moves from plain cited answers to structured, verifiable claims grounded in source evidence.

## Build Only This

- structured claim schema
- `CitationVerifier`
- claim-to-source mapping
- simple support verifier interface
- deterministic numeric/date checks
- one-regeneration-attempt cap
- refusal after second verification failure
- `docs/youtube/phase-09.md`

Do not build confidence scoring in this slice.

## Requirements

Implement this required flow:

```text
evidence context
→ structured claims JSON
→ citation verification
→ final rendered answer
```

Implementation requirements:

- Define a structured claim schema.
- Every claim must include source IDs.
- Map claims to cited source evidence.
- Implement `CitationVerifier`.
- Add a simple support verifier interface.
- Reject fake citations.
- Reject missing citations.
- Reject claims that cite sources that do not support them.
- Add deterministic numeric checks.
- Add deterministic date checks.
- If verification fails, allow at most one regeneration attempt.
- If verification fails a second time, refuse instead of returning unsupported claims.
- Include useful verification details in `/query/debug`.

## API Endpoints Required

No brand-new HTTP endpoint is required.

Update:

```http
POST /query
POST /query/debug
```

`POST /query` must return the final rendered answer only after citation verification succeeds, or refusal after repeated failure.

`POST /query/debug` must include structured claim and verification details.

## Tests Required

Add tests for:

- claim has source IDs
- fake citation rejected
- missing citation rejected
- wrong number rejected
- wrong date rejected
- unsupported claim fails
- retry cap works
- second failure refuses

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/query/debug \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What number is mentioned?\"}"

pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-09.md
```

The documentation must include:

- phase title: `Phase 09 — Structured Claims and Citation Verification`
- video goal
- structured claim schema explanation
- claim-to-source mapping walkthrough
- citation verifier explanation
- numeric and date check demo
- retry and refusal behavior
- debug trace demo
- test commands
- validation checklist

## Acceptance Criteria

- Answers are generated through structured claims.
- Claims include source IDs.
- Fake and missing citations are rejected.
- Wrong numbers and dates are rejected by deterministic checks.
- Unsupported claims fail verification.
- Regeneration is capped at one retry.
- A second verification failure returns refusal.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 09.

Do not implement confidence scoring, full evaluation, production adapters, or UI.

Do not implement any future slice.
