# Robust Local RAG Engine

Local-first RAG engine built one vertical slice at a time.

## Current Slice

Slice 00 creates the project foundation:

- FastAPI application entry point
- application config
- structured logging
- `/health` endpoint
- pytest setup
- base package folders
- phase documentation

RAG ingestion, retrieval, answering, verification, and UI features are intentionally not implemented yet.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload
```

Health check:

```powershell
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

## Test

```powershell
pytest
```

## Codex Vertical Slice Workflow

Generate an active prompt:

```powershell
.\scripts\run_slice.ps1 `
  -SliceId "slice-00" `
  -SliceFile "docs/codex/slices/slice-00-project-foundation.md"
```

Then paste `docs/codex/ACTIVE_PROMPT.md` into Codex.

Run the gate:

```powershell
.\scripts\run_gate.ps1 -Slice "slice-00"
```

Commit the slice:

```powershell
.\scripts\commit_slice.ps1 `
  -Slice "slice-00" `
  -Message "Slice 00: project foundation"
```
