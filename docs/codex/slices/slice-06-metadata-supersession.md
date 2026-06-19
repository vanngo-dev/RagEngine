# Slice 06 — Metadata Filters and Supersession

## Goal

Add document metadata filtering and active/superseded lifecycle.

This slice makes retrieval respect document metadata and stale-source status.

## Build Only This

- metadata fields
- `document_family_id`
- active/superseded status
- `POST /documents/{document_id}/supersede`
- `include_superseded` filter
- metadata filters for vector, keyword, and hybrid search
- `docs/youtube/phase-06.md`

Do not build reranking or claim verification in this slice.

## Requirements

Add these required document fields:

```text
document_family_id
entity
document_type
document_date
status
superseded_by_document_id
```

Implementation requirements:

- Support active and superseded document lifecycle.
- Hide superseded documents from search results by default.
- Allow callers to include superseded documents with `include_superseded`.
- Add metadata filters to vector search.
- Add metadata filters to keyword search.
- Add metadata filters to hybrid search.
- Ensure supersession updates document status consistently.
- Preserve existing upload, chunk, embedding, search, and query behavior.
- Keep migrations or schema setup simple for local SQLite.

## API Endpoints Required

Implement:

```http
POST /documents/{document_id}/supersede
```

Request body:

```json
{
  "new_document_id": "replacement_doc_id"
}
```

Update these existing search endpoints to accept metadata filters and `include_superseded`:

```http
POST /search/vector
POST /search/keyword
POST /search/hybrid
```

## Tests Required

Add tests for:

- superseded document hidden by default
- `include_superseded` returns old document
- metadata filters apply to vector search
- metadata filters apply to keyword search
- metadata filters apply to hybrid search

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/documents/{document_id}/supersede \
  -H "Content-Type: application/json" \
  -d "{\"new_document_id\":\"replacement_doc_id\"}"

pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-06.md
```

The documentation must include:

- phase title: `Phase 06 — Metadata Filters and Supersession`
- video goal
- metadata field explanation
- active vs superseded lifecycle explanation
- `include_superseded` behavior
- filtered search demo
- supersession demo
- test commands
- validation checklist

## Acceptance Criteria

- Documents include the required metadata fields.
- Superseded documents are excluded from search by default.
- `include_superseded` can return older superseded documents.
- Metadata filters work for vector search.
- Metadata filters work for keyword search.
- Metadata filters work for hybrid search.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 06.

Do not implement reranking, evidence selection, prompt-injection defense, structured claim verification, confidence scoring, full evaluation, production adapters, or UI.

Do not implement any future slice.
