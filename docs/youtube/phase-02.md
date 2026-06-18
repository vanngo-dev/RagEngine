# Phase 02 — First Searchable RAG Retrieval

## Video Goal

Make uploaded documents searchable with deterministic local embeddings and a simple vector index.

## Embedding Provider Interface

The retrieval layer now has an `EmbeddingProvider` interface with a deterministic fake provider for tests and a placeholder local provider for a future real embedding backend.

## Why Embedding Text Is Embedded

Chunks keep raw `text` clean for citation and display. The embedding pipeline uses `embedding_text`, which adds document title, document type, and section context so retrieval has more useful semantic signals.

## Vector Index Flow

`POST /documents/{document_id}/embed` loads chunks, embeds each chunk's `embedding_text`, and stores vectors with `chunk_id`, `document_id`, `section_title`, and document `status`.

`POST /search/vector` embeds the query, compares it to stored vectors, and returns ranked chunks with text and metadata.

## Search Endpoint Demo

```bash
curl -X POST http://localhost:8000/documents/{document_id}/embed

curl -X POST http://localhost:8000/search/vector \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"What is this document about?\",\"top_k\":5}"
```

## Lightweight Eval Demo

```bash
python -m rag_engine.evals.lightweight_eval
```

The first eval reports `recall_at_k` over `data/evals/gold_lite.jsonl`.

## Test Commands

```bash
pytest
```

## Validation Checklist

- fake embeddings are deterministic
- embedding uses `embedding_text`
- vector index stores chunks
- vector search retrieves chunks
- search results include text and metadata
- `recall@k` calculation works
