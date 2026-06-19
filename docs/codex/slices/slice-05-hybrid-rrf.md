# Slice 05 — Hybrid Retrieval With RRF

## Goal

Add keyword search and combine it with vector search using Reciprocal Rank Fusion.

This slice improves retrieval by combining lexical and semantic candidates.

## Build Only This

- SQLite FTS5 keyword index
- `POST /search/keyword`
- `POST /search/hybrid`
- Reciprocal Rank Fusion
- vector vs keyword vs hybrid eval comparison
- `docs/youtube/phase-05.md`

Do not build reranking or evidence selection in this slice.

## Requirements

Implement hybrid retrieval with this flow:

```text
run keyword top 50
run vector top 50
merge with RRF
remove duplicates
return ranked candidates
```

Implementation requirements:

- Add a SQLite FTS5 keyword index over chunks.
- Keep keyword indexing in sync with stored chunks.
- Support exact phrase search behavior where SQLite FTS5 can provide it.
- Implement Reciprocal Rank Fusion deterministically.
- Merge duplicate `chunk_id` results into one candidate.
- Return ranked candidates with text, metadata, and ranking signals.
- Update lightweight eval to record vector, keyword, and hybrid scores.
- Preserve existing vector search behavior.

## API Endpoints Required

Implement:

```http
POST /search/keyword
POST /search/hybrid
```

Both endpoints must accept:

```json
{
  "query": "risk factors",
  "top_k": 10
}
```

`POST /search/keyword` must return keyword-ranked chunks.

`POST /search/hybrid` must return RRF-ranked hybrid candidates.

## Tests Required

Add tests for:

- FTS search works
- exact phrase search works
- RRF output deterministic
- duplicate chunk IDs merged
- hybrid search returns candidates from both systems
- eval records vector vs hybrid score

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/search/keyword \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"risk factors\",\"top_k\":10}"

curl -X POST http://localhost:8000/search/hybrid \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"risk factors\",\"top_k\":10}"

python -m rag_engine.evals.lightweight_eval
pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-05.md
```

The documentation must include:

- phase title: `Phase 05 — Hybrid Retrieval With RRF`
- video goal
- keyword search overview
- vector vs keyword retrieval comparison
- RRF explanation
- hybrid endpoint demo
- eval comparison demo
- test commands
- validation checklist

## Acceptance Criteria

- Keyword search works through SQLite FTS5.
- Hybrid search runs keyword and vector retrieval.
- Reciprocal Rank Fusion is deterministic.
- Duplicate chunk IDs are merged.
- Hybrid eval results compare vector, keyword, and hybrid retrieval.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 05.

Do not implement reranking, evidence selection, prompt-injection defense, structured claim verification, confidence scoring, full evaluation, production adapters, or UI.

Do not implement any future slice.
