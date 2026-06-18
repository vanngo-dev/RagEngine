# Phase 10 — Confidence and Refusal

## Video Goal

Add deterministic confidence scoring and refusal behavior based on evidence quality.

## Confidence Signals

Positive signals include direct evidence, verified citations, high reranker score, multiple agreeing sources, and exact phrase matches.

Negative signals include missing evidence, failed citations, unresolved conflicts, weak retrieval, and prompt-injection warnings.

## Refusal Policy

The engine refuses when confidence is low, evidence is missing, or citations fail verification. Refusal responses include missing information explaining what was not strong enough.

## No-Answer Case Demo

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"Question not supported by the corpus\"}"
```

## False-Confidence Metric

The lightweight eval now includes a starter `false_confidence_rate` for no-answer cases.

## Query Response Demo

`/query` now returns:

```text
confidence
confidence_label
refusal
missing_information
```

## Test Commands

```bash
pytest
```

## Validation Checklist

- strong evidence raises confidence
- weak evidence lowers confidence
- unsupported questions refuse
- failed citations lower confidence
- conflicts lower confidence
- prompt-injection warnings lower confidence
