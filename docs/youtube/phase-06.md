# Phase 06 — Metadata Filters and Supersession

## Video Goal

Add document metadata filters and active/superseded lifecycle behavior to retrieval.

## Metadata Fields

Documents now include:

- `document_family_id`
- `entity`
- `document_type`
- `document_date`
- `status`
- `superseded_by_document_id`

## Active vs Superseded

New uploads are active by default. Superseding a document marks the old document as `superseded`, points it at the replacement document, and keeps the replacement active.

## Include Superseded Behavior

Search endpoints hide superseded documents by default. Set `include_superseded` to `true` to include older documents for historical queries.

## Filtered Search Demo

```bash
curl -X POST http://localhost:8000/search/hybrid \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"risk factors\",\"entity\":\"Acme\",\"document_type\":\"policy\",\"top_k\":10}"
```

## Supersession Demo

```bash
curl -X POST http://localhost:8000/documents/{document_id}/supersede \
  -H "Content-Type: application/json" \
  -d "{\"new_document_id\":\"replacement_doc_id\"}"
```

## Test Commands

```bash
pytest
```

## Validation Checklist

- documents include metadata fields
- superseded documents are hidden by default
- `include_superseded` returns older documents
- vector search supports metadata filters
- keyword search supports metadata filters
- hybrid search supports metadata filters
