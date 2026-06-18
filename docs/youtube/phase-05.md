# Phase 05 — Hybrid Retrieval With RRF

## Video Goal

Add keyword retrieval with SQLite FTS5 and combine keyword plus vector candidates using Reciprocal Rank Fusion.

## Keyword Search Overview

Chunk text is indexed into a SQLite FTS5 table when chunks are created. `POST /search/keyword` runs FTS search and returns ranked chunks with text and metadata.

## Vector vs Keyword Retrieval

Vector search handles semantic similarity through embeddings. Keyword search handles exact terms and phrases. Hybrid search uses both so a query can benefit from lexical matches and embedding similarity.

## RRF Explanation

Reciprocal Rank Fusion scores each candidate by rank rather than raw score:

```text
score += 1 / (k + rank)
```

This avoids directly comparing vector similarity scores with keyword BM25 scores.

## Hybrid Endpoint Demo

```bash
curl -X POST http://localhost:8000/search/keyword \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"risk factors\",\"top_k\":10}"

curl -X POST http://localhost:8000/search/hybrid \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"risk factors\",\"top_k\":10}"
```

## Eval Comparison Demo

```bash
python -m rag_engine.evals.lightweight_eval
```

The result includes vector, keyword, and hybrid recall fields.

## Test Commands

```bash
pytest
```

## Validation Checklist

- FTS search works
- exact phrase search works
- RRF is deterministic
- duplicate chunk IDs merge
- hybrid results include ranking signals
- eval records vector, keyword, and hybrid scores
