# Phase 09 — Structured Claims and Citation Verification

## Video Goal

Generate structured claims, verify cited support, and refuse after repeated verification failure.

## Structured Claim Schema

Answers are converted into structured claims with:

- `claim_id`
- `claim_text`
- `source_ids`

Every claim must cite at least one source ID.

## Claim-To-Source Mapping

Citation verification maps each claim's source IDs back to the source blocks used in the prompt. Fake or missing source IDs fail verification.

## Citation Verifier

`CitationVerifier` checks that citations exist, that cited source text supports the claim, and that deterministic number/date checks pass.

## Numeric and Date Checks

Numbers and ISO-style dates in claims must appear in the cited source text. This catches simple wrong-number and wrong-date claims before rendering.

## Retry and Refusal

If verification fails, the engine allows one regeneration attempt. If the second attempt also fails, `/query` returns refusal instead of unsupported claims.

## Debug Trace Demo

```bash
curl -X POST http://localhost:8000/query/debug \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"What number is mentioned?\"}"
```

The debug response includes `structured_claims`, `verification`, and `verification_attempts`.

## Test Commands

```bash
pytest
```

## Validation Checklist

- claims include source IDs
- fake citations are rejected
- missing citations are rejected
- wrong numbers are rejected
- wrong dates are rejected
- unsupported claims fail
- retry is capped at one regeneration
- second verification failure refuses
