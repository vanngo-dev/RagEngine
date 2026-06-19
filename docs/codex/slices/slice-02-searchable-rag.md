# Slice 02 — First Searchable RAG Retrieval

## Goal

Make uploaded documents searchable with local embeddings and vector search.

This slice adds the first retrieval capability over chunks created by the document pipeline.

## Build Only This

- `EmbeddingProvider` interface
- deterministic fake embedding provider for tests
- local embedding provider placeholder
- LanceDB vector index adapter or simple local vector adapter
- `POST /documents/{document_id}/embed`
- `POST /search/vector`
- lightweight `recall@k` eval CLI
- `data/evals/gold_lite.jsonl`
- `docs/youtube/phase-02.md`

Do not build LLM answering in this slice.

## Requirements

Implement vector retrieval with these requirements:

- Use `chunk.embedding_text` for embeddings.
- Do not embed the raw `chunk.text` field directly.
- Store vector payload with `chunk_id`, `document_id`, `section_title`, and `status`.
- Return search results with chunk `text` and metadata.
- Add a deterministic fake embedding provider for tests.
- Add a local embedding provider placeholder that makes future real local embeddings easy to add.
- Add a vector index adapter using LanceDB or a simple local vector adapter.
- Keep vector operations deterministic in tests.
- Add CLI entry point:

```bash
python -m rag_engine.evals.lightweight_eval
```

- Add initial eval data:

```text
data/evals/gold_lite.jsonl
```

## API Endpoints Required

Implement:

```http
POST /documents/{document_id}/embed
POST /search/vector
```

`POST /documents/{document_id}/embed` must embed all chunks for a stored document.

`POST /search/vector` must accept:

```json
{
  "query": "What is this document about?",
  "top_k": 5
}
```

The vector search response must include ranked results with text and metadata.

## Tests Required

Add tests for:

- fake embedding provider returns stable vectors
- embedding uses `embedding_text`
- vector index stores chunks
- vector search retrieves chunks
- metadata returned in search results
- `recall@k` calculation works

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/documents/{document_id}/embed

curl -X POST http://localhost:8000/search/vector \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What is this document about?\",\"top_k\":5}"

python -m rag_engine.evals.lightweight_eval
pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-02.md
```

The documentation must include:

- phase title: `Phase 02 — First Searchable RAG Retrieval`
- video goal
- embedding provider interface overview
- why `embedding_text` is embedded instead of raw text
- vector index flow
- search endpoint demo
- lightweight eval demo
- test commands
- validation checklist

## Acceptance Criteria

- Chunks can be embedded through `POST /documents/{document_id}/embed`.
- Embeddings are generated from `embedding_text`.
- Vector search returns relevant chunks with text and metadata.
- The fake embedding provider is deterministic.
- The lightweight eval CLI runs and reports `recall@k`.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 02.

Do not implement LLM answer generation, `/query`, hybrid retrieval, keyword search, reranking, citation verification, confidence scoring, full evaluation, production adapters, or UI.

Do not implement any future slice.
