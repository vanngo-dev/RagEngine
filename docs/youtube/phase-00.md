# Phase 00 — Project Foundation

## Video Goal

Set up the base FastAPI RAG engine project with config, structured logging, a health endpoint, and tests.

## Why This Matters

Every later RAG slice needs a stable app entry point, predictable configuration, and a fast test loop before document processing or retrieval exists.

## What We Build

- FastAPI app
- application settings
- structured logging
- `/health` endpoint
- pytest setup
- base package and data folders

## Manual Demo

Start the API:

```bash
uvicorn app.main:app --reload
```

Check health:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "rag-engine",
  "version": "0.1.0"
}
```

## Test Commands

```bash
pytest
```

## Common Mistakes

- Running commands outside the repository root
- Missing Python dependencies
- Using the wrong Uvicorn import path
- Running on a port already in use

## Validation Checklist

- App imports successfully
- `/health` returns HTTP 200
- `/health` returns `status: ok`
- `pytest` passes
