# Slice 00 — Project Foundation

## Goal

Create the base FastAPI project for the robust local RAG engine.

This slice establishes the minimum runnable project skeleton that all later slices will build on.

## Build Only This

- FastAPI app
- config
- structured logging
- pytest setup
- health endpoint
- base folder structure
- README
- `docs/youtube/phase-00.md`

Do not build any RAG features in this slice.

## Requirements

Create the following folder structure if it does not already exist:

```text
app/
  main.py
  config.py
  dependencies.py

api/
  routes_health.py

rag_engine/
  __init__.py
  ingestion/
    __init__.py
  retrieval/
    __init__.py
  generation/
    __init__.py
  verification/
    __init__.py
  evals/
    __init__.py
  storage/
    __init__.py
  models/
    __init__.py

tests/
  unit/
  integration/

docs/
  youtube/

data/
  raw/
  processed/
  evals/
```

Implement the project foundation with these requirements:

- Create `app/main.py` with a FastAPI application instance.
- Create `app/config.py` for application settings.
- Create `app/dependencies.py` for future dependency wiring, even if it is minimal now.
- Create `api/routes_health.py` for the health route.
- Register the health route in the FastAPI app.
- Add basic structured logging that is safe for local development.
- Add pytest configuration if the repository does not already have it.
- Add or update `README.md` with setup, run, and test commands for this slice.
- Keep implementation simple and local-only.

## API Endpoints Required

Implement:

```http
GET /health
```

Expected response:

```json
{
  "status": "ok",
  "service": "rag-engine",
  "version": "0.1.0"
}
```

## Tests Required

Create:

```text
tests/unit/test_config.py
tests/integration/test_health.py
```

Tests must verify:

- config loads successfully
- the FastAPI app imports successfully
- `GET /health` returns HTTP 200
- `GET /health` returns `status: ok`
- `GET /health` returns `service: rag-engine`
- `GET /health` returns a `version` value

## Manual Validation

Run:

```bash
uvicorn app.main:app --reload
curl http://localhost:8000/health
pytest
```

## YouTube Documentation

Create:

```text
docs/youtube/phase-00.md
```

The documentation must include:

- phase title: `Phase 00 — Project Foundation`
- video goal
- why this foundation matters
- what is built in this slice
- manual demo steps
- test commands
- common mistakes
- validation checklist

## Acceptance Criteria

- `uvicorn app.main:app --reload` starts successfully.
- `curl http://localhost:8000/health` returns the expected JSON response.
- `pytest` passes.
- `README.md` exists and documents setup, run, and test commands.
- `docs/youtube/phase-00.md` exists.
- No document upload, parsing, embedding, retrieval, generation, verification, or UI behavior exists.

## Do Not Continue

Stop after completing Slice 00.

Do not implement document upload, embeddings, vector search, keyword search, LLM answering, RAG query endpoints, evaluation harnesses, production adapters, or UI.

Do not implement any future slice.
