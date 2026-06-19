# Phase 13A — Shared Web UI

## Video Goal

Add one shared React and TypeScript web UI for the FastAPI RAG backend.

## What Changed

- Added `frontend/` with Vite, React, TypeScript, and plain CSS.
- Added a fetch-based API client that defaults to `http://127.0.0.1:8000`.
- Added panels for backend status, upload, document listing, chunk viewing, embedding/indexing, questions, answers, citations, and debug traces.
- Added defensive UI states for offline backend, empty documents, empty chunks, failed uploads, failed queries, failed debug traces, and unexpected JSON shapes.
- Added minimal development CORS support for Vite origins.

## Validation

```powershell
python -m pytest -q
cd frontend
npm install
npm run build
```

## Local Demo Flow

1. Start the backend with `python -m uvicorn app.main:app --reload`.
2. Start the UI with `cd frontend` and `npm run dev`.
3. Open `http://127.0.0.1:5173`.
4. Upload a `.txt` or `.md` file.
5. Select the document, embed/index it, ask a question, and inspect citations plus debug trace.

## Known Limitations

- The web UI assumes the backend is already running.
- Authentication, multi-user sessions, and packaged deployment are future work.
- Production adapter wiring remains separate from the LocalLite web flow.
