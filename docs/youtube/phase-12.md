# Phase 12 — Production Adapter Interfaces

## Video Goal

Introduce adapter boundaries for future PostgreSQL, Qdrant, OpenSearch, and Redis-backed jobs while keeping LocalLite working.

## Interface Boundary

The engine now defines interfaces for:

- `DocumentStore`
- `ChunkStore`
- `VectorIndex`
- `KeywordIndex`
- `JobStore`
- `EmbeddingProvider`
- `LLMProvider`
- `RerankerProvider`
- `CitationVerifier`

## Storage Profile Config

The default storage profile is:

```text
STORAGE_PROFILE=local_lite
```

LocalLite continues to use SQLite-backed document/chunk storage, SQLite-backed vector storage, and SQLite FTS5 keyword search.

## LocalLite Preservation Demo

Existing upload, embed, search, query, debug, and eval tests still run through the LocalLite adapter factories.

## Placeholder Adapter Behavior

The placeholder adapters are:

- `postgres`
- `qdrant`
- `opensearch`
- `redis_jobs`

Selecting one before implementation raises a clear `NotImplementedError`.

## Test Commands

```bash
pytest
```

## Validation Checklist

- required interfaces exist
- `STORAGE_PROFILE=local_lite` loads
- LocalLite works through interface factories
- placeholder adapters raise clear errors
- no real PostgreSQL, Qdrant, OpenSearch, or Redis logic exists
