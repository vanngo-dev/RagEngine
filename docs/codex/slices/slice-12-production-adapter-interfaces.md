# Slice 12 — Production Adapter Interfaces

## Goal

Prepare the engine for PostgreSQL, Qdrant, OpenSearch, and background jobs without breaking LocalLite mode.

This slice introduces adapter boundaries while keeping local development behavior intact.

## Build Only This

- storage interfaces
- adapter boundaries
- config switch for storage profile
- LocalLite implementation behind interfaces
- placeholder production adapters
- `docs/youtube/phase-12.md`

Do not implement real production storage or queue logic in this slice.

## Requirements

Create these required interfaces:

```text
DocumentStore
ChunkStore
VectorIndex
KeywordIndex
JobStore
EmbeddingProvider
LLMProvider
RerankerProvider
CitationVerifier
```

Add this required config value:

```text
STORAGE_PROFILE=local_lite
```

Create placeholder adapters:

```text
postgres
qdrant
opensearch
redis_jobs
```

Implementation requirements:

- Route LocalLite behavior through the new interfaces.
- Preserve all existing local functionality.
- Keep `local_lite` as the default storage profile.
- Add a clean config switch for storage profile selection.
- Add placeholder production adapters with clear boundaries.
- Placeholder adapters must raise clear `NotImplementedError` if selected before implementation.
- Do not add real PostgreSQL logic.
- Do not add real Qdrant logic.
- Do not add real OpenSearch logic.
- Do not add real Redis job logic.
- Keep existing tests passing.

## API Endpoints Required

No new HTTP endpoints are required.

Existing endpoints must continue to work in `local_lite` mode through the new interfaces.

## Tests Required

Add tests for:

- LocalLite still works through interfaces
- storage profile loads
- placeholder adapter raises clear error
- existing tests still pass

## Manual Validation

Run:

```bash
pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-12.md
```

The documentation must include:

- phase title: `Phase 12 — Production Adapter Interfaces`
- video goal
- interface boundary explanation
- storage profile config explanation
- LocalLite preservation demo
- placeholder adapter behavior
- test commands
- validation checklist

## Acceptance Criteria

- Required interfaces exist.
- `STORAGE_PROFILE=local_lite` is supported.
- LocalLite behavior still works through interfaces.
- Placeholder production adapters exist.
- Selecting an unimplemented production adapter raises a clear `NotImplementedError`.
- Existing tests still pass.
- No real PostgreSQL, Qdrant, OpenSearch, or Redis logic is implemented.

## Do Not Continue

Stop after completing Slice 12.

Do not implement actual PostgreSQL, Qdrant, OpenSearch, Redis, background workers, deployment logic, or UI.

Do not implement any future slice.
