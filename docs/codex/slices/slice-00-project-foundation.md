@'
# Slice 00 — Project Foundation

## Goal

Create the base FastAPI project for the robust local RAG engine.

## Build Only This

- FastAPI app
- config
- structured logging
- pytest setup
- health endpoint
- base folder structure
- docs/youtube/phase-00.md

## Required Folder Structure

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

## Required Endpoint

GET /health

Expected response:

{
  "status": "ok",
  "service": "rag-engine",
  "version": "0.1.0"
}

## Requirements

1. Create app/main.py.
2. Create app/config.py using pydantic-settings.
3. Create api/routes_health.py.
4. Register the health route in the FastAPI app.
5. Add basic structured logging.
6. Add requirements.txt.
7. Add pytest setup.
8. Add unit test for config loading.
9. Add integration test for /health.
10. Add README.md with setup, run, and test commands.
11. Add docs/youtube/phase-00.md.

## Suggested Dependencies

fastapi
uvicorn
pydantic
pydantic-settings
pytest
httpx
python-dotenv

## Tests Required

tests/unit/test_config.py
tests/integration/test_health.py

Tests must verify:

- config loads
- app imports successfully
- GET /health returns 200
- GET /health returns status = ok
- service name is rag-engine
- version exists

## Manual Validation Commands

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
curl http://localhost:8000/health
pytest

## YouTube Tutorial Documentation

Create:

docs/youtube/phase-00.md

Include:

# Phase 00 — Project Foundation

## Video Goal
Set up the base FastAPI RAG engine project with config, logging, health endpoint, and tests.

## Why This Matters
Every later RAG slice needs a stable, testable foundation.

## What We Build
- FastAPI app
- config
- logging
- health endpoint
- pytest setup

## Manual Demo
Show the server running and /health returning status ok.

## Test Commands
pytest

## Common Mistakes
- Wrong Python environment
- Uvicorn import path error
- Missing dependency
- Port already in use

## Validation Checklist
- App starts
- /health returns 200
- Tests pass

## Acceptance Criteria

- uvicorn app.main:app --reload starts successfully.
- curl http://localhost:8000/health returns status ok.
- pytest passes.
- README.md exists.
- docs/youtube/phase-00.md exists.
- No RAG functionality is implemented yet.

## Final Response Required

At the end, report:

1. Files created or modified.
2. Tests added.
3. Tests run.
4. Manual validation commands.
5. Known limitations.
6. Recommended git commit message.

Recommended commit message:

Slice 00: project foundation

## Do Not Continue

Do not implement document upload.
Do not implement embeddings.
Do not implement vector search.
Do not implement LLM answering.
Do not implement RAG yet.
Do not implement UI.
Stop after this slice.
'@ | Set-Content -Encoding UTF8 docs\codex\slices\slice-00-project-foundation.md