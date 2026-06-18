# Phase 01 — Minimal Document Pipeline

## Video Goal

Upload `.txt` and `.md` files, store them locally, parse them, chunk them, and prepare contextual `embedding_text` for later retrieval slices.

## Upload Flow Overview

The upload endpoint accepts a multipart file, validates the extension, reads the content, computes a SHA-256 hash, stores the raw file under `data/raw/{document_id}/`, records document metadata in SQLite, parses the text, and stores chunks linked to the document.

## SQLite Document and Chunk Storage

Documents are stored with stable metadata such as `id`, `title`, `file_name`, `file_path`, `source_type`, `content_hash`, `status`, `created_at`, and `updated_at`.

Chunks are stored separately with `chunk_id`, `document_id`, `text`, `embedding_text`, `section_title`, `chunk_index`, `token_count`, and `created_at`.

## Parser and Chunker

The `.txt` parser splits paragraph text on blank lines. The `.md` parser tracks headings and attaches the current heading as each paragraph's section title.

The chunker keeps paragraph content clean and stores artificial context only in `embedding_text`, not in the raw chunk `text`.

## Embedding Text

Each chunk stores `embedding_text` in this format:

```text
Document: {title}
Document Type: {source_type}
Section: {section_title}

{text}
```

## Manual Demo

Upload a Markdown file:

```bash
curl -X POST http://localhost:8000/documents/upload -F "file=@sample.md"
```

List documents:

```bash
curl http://localhost:8000/documents
```

List chunks:

```bash
curl http://localhost:8000/documents/{document_id}/chunks
```

## Test Commands

```bash
pytest
```

## Validation Checklist

- `.txt` uploads work
- `.md` uploads work
- unsupported extensions are rejected
- duplicate hashes are detected
- chunks are linked to `document_id`
- `embedding_text` includes title, type, and section
- chunk `text` has no artificial context header
