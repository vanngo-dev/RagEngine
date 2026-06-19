# Slice 01 — Minimal Document Pipeline

## Goal

Upload, store, parse, and chunk `.txt` and `.md` files.

This slice turns the project foundation into a minimal document ingestion pipeline without search, embeddings, or answering.

## Build Only This

- `POST /documents/upload`
- SQLite document store
- SQLite chunk store
- `.txt` parser
- `.md` parser
- simple paragraph-aware chunker
- `embedding_text` generation
- `GET /documents`
- `GET /documents/{document_id}/chunks`
- `docs/youtube/phase-01.md`

Do not build retrieval or generation in this slice.

## Requirements

Add a local document pipeline with these document fields:

```text
id
title
file_name
file_path
source_type
content_hash
status
created_at
updated_at
```

Add a local chunk store with these chunk fields:

```text
chunk_id
document_id
text
embedding_text
section_title
chunk_index
token_count
created_at
```

Generate `embedding_text` exactly in this format:

```text
Document: {title}
Document Type: {source_type}
Section: {section_title}

{text}
```

Implementation requirements:

- Accept only `.txt` and `.md` uploads.
- Store uploaded raw files in a local data directory.
- Compute a stable content hash for duplicate detection.
- Reject unsupported file extensions with a clear error.
- Detect duplicate content hashes and avoid creating duplicate documents.
- Parse text from `.txt` and `.md` files.
- Chunk documents with paragraph awareness.
- Preserve clean chunk `text` without artificial context headers.
- Store the generated `embedding_text` separately from `text`.
- Link every chunk to its parent `document_id`.
- Keep this slice deterministic and suitable for tests.

## API Endpoints Required

Implement:

```http
POST /documents/upload
GET /documents
GET /documents/{document_id}/chunks
```

`POST /documents/upload` must accept multipart file upload.

`GET /documents` must return stored document metadata.

`GET /documents/{document_id}/chunks` must return chunks linked to the requested document.

## Tests Required

Add tests for:

- upload `.txt` file
- upload `.md` file
- unsupported file rejected
- duplicate hash detected
- chunks created
- chunks linked to `document_id`
- `embedding_text` includes title, type, and section
- `text` field does not contain artificial context header

## Manual Validation

Run:

```bash
curl -X POST http://localhost:8000/documents/upload -F "file=@sample.md"
curl http://localhost:8000/documents
curl http://localhost:8000/documents/{document_id}/chunks
pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-01.md
```

The documentation must include:

- phase title: `Phase 01 — Minimal Document Pipeline`
- video goal
- upload flow overview
- SQLite document and chunk storage explanation
- parser and chunker explanation
- `embedding_text` explanation
- manual demo steps
- test commands
- validation checklist

## Acceptance Criteria

- `.txt` and `.md` files can be uploaded.
- Uploaded documents are stored with the required metadata.
- Chunks are created and linked to their source document.
- Duplicate content is detected by hash.
- Unsupported file types are rejected.
- `embedding_text` contains context needed for future embedding.
- Raw chunk `text` stays free of artificial context headers.
- All tests for this slice pass.

## Do Not Continue

Stop after completing Slice 01.

Do not implement embeddings, vector search, keyword search, hybrid retrieval, LLM answering, RAG query endpoints, citation handling, evaluation harnesses, production adapters, or UI.

Do not implement any future slice.
