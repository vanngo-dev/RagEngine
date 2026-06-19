# Robust Local RAG Engine

## Overview

Robust Local RAG Engine is a local-first backend for accurate, reliable, source-grounded answers from private documents. It is designed as an evidence system, not a generic chatbot.

The engine is built to ingest documents, parse and chunk them, create searchable indexes, retrieve relevant evidence, generate cited answers, verify citations, refuse unsupported answers, run evaluations, and connect to a web or desktop UI later.

## Project Goal

The goal is to build an evidence-based RAG engine that can become Pareto-frontier within a niche domain by combining clean document ingestion, strong metadata, hybrid retrieval, reranking, citation verification, confidence scoring, refusal behavior, and evaluation.

This project is not trying to make a broad conversational assistant first. It builds the reliability layer that a useful assistant would depend on.

## What Problem This Solves

Common RAG systems often fail because they produce hallucinated answers, weak citations, stale-document answers, poor chunks, vector-only retrieval misses, no refusal behavior, no eval harness, and no debug trace.

This engine addresses those problems by storing document metadata, separating raw chunk text from contextualized embedding text, using vector plus keyword retrieval, applying hybrid RRF ranking, reranking evidence, verifying cited claims, checking numbers and dates, tracking confidence, refusing weak answers, and exposing debug/eval traces.

## Core Philosophy

Bad RAG says: "It sounds right."

Better RAG says: "Here is an answer with sources."

Reliable RAG says: "Here is the answer, the evidence, verified citations, confidence, limitations, and trace."

## Key Features

- Document upload for `.txt` and `.md`
- SQLite document registry
- Paragraph-aware chunking
- Contextualized `embedding_text`
- Vector retrieval
- Keyword retrieval with SQLite FTS5
- Hybrid retrieval with Reciprocal Rank Fusion
- Query endpoint
- Debug query endpoint
- Citation support
- Structured claims
- Confidence and refusal fields
- Lightweight and full evaluation harnesses
- LocalLite implementation
- Adapter interface preparation

## Reliability Features

- Source-grounded answers
- Empty-context refusal
- Prompt-injection defense for retrieved documents
- Claim-level citation verification
- Numeric and date checks
- Metadata filtering
- Active/superseded document lifecycle
- Debug trace
- Eval metrics
- False-confidence awareness

## Architecture

```text
Document Upload
  -> Document Registry
  -> Parser
  -> Chunker
  -> Embedding Pipeline
  -> Vector Index
  -> Keyword Index
  -> Hybrid Retriever
  -> Reranker / Evidence Selector
  -> Context Builder
  -> LLM Provider
  -> Claim / Citation Verifier
  -> Confidence / Refusal
  -> Final Answer
```

Main package areas:

- `app/`: FastAPI application setup, config, dependencies, logging
- `api/`: HTTP route modules
- `frontend/`: shared React and TypeScript UI for web and future desktop wrapper
- `rag_engine/ingestion/`: parsing, chunking, upload pipeline
- `rag_engine/retrieval/`: embeddings, vector search, keyword search, hybrid search, reranking
- `rag_engine/generation/`: context building, prompts, LLM providers, answer flow
- `rag_engine/verification/`: structured claims, citation verification, confidence scoring
- `rag_engine/evals/`: lightweight and full eval runners
- `rag_engine/storage/`: SQLite LocalLite storage and adapter factories

## LocalLite Stack

The current implementation is a lightweight local backend:

- FastAPI
- SQLite
- SQLite FTS5
- SQLite-backed local vector adapter
- Deterministic fake embedding provider for tests
- Mock LLM provider by default
- Ollama-compatible LLM provider
- Pytest

Production adapter skeletons exist for PostgreSQL, Qdrant, OpenSearch, and Redis-backed job storage behind `STORAGE_PROFILE=production`. These are not full production implementations yet; selecting production mode without optional dependencies raises a clear configuration error. LocalLite remains the default working profile.

The project now includes a shared React web UI in `frontend/`. The UI connects to the FastAPI backend and is intended to be reused by the desktop shell rather than forked into a separate app.

## Current Project Status

This is a LocalLite RAG Engine v0.1 backend with a shared web UI, a Tauri desktop wrapper, and production adapter skeletons.

It is not yet a full packaged desktop or production web product.

The backend engine is slice-12 complete if tests pass.

## What Is Complete

- FastAPI backend with `GET /health`
- Upload and storage for `.txt` and `.md`
- SQLite document and chunk storage
- Document metadata fields and supersession
- Chunk generation and contextualized embedding text
- Deterministic fake embeddings for local tests
- SQLite-backed vector index
- SQLite FTS5 keyword index
- Vector, keyword, and hybrid search endpoints
- RRF-based hybrid retrieval
- Reranker provider interface and mock reranker
- Evidence selector with simple diversity and conflict flags
- Query endpoint with cited answer generation
- Debug endpoint with retrieval, prompt, evidence, warning, claim, verification, and confidence trace fields
- Prompt-injection warning detection and untrusted source wrapper
- Structured claim extraction
- Citation, numeric, and date verification
- Confidence scoring and refusal behavior
- Lightweight eval CLI
- Full eval CLI with JSON reports and regression comparison support
- LocalLite adapter factories and production adapter skeletons
- Production profile configuration for PostgreSQL, Qdrant, OpenSearch, and Redis
- Production Docker Compose service stack and environment example
- Shared Vite React web UI for backend health, document upload, indexing, querying, citations, and debug traces
- Tauri desktop wrapper around the shared React UI
- Local and production release verification scripts and docs
- Slice phase documentation in `docs/youtube/`

## What Is Not Complete Yet

- Real PostgreSQL, Qdrant, OpenSearch, or Redis implementations
- Packaged installer or release bundle
- Large-scale document ingestion hardening
- Advanced aggregate or map-reduce RAG
- Domain-specific adapter tuning
- Production-grade auth, deployment, monitoring, and operations

## API Overview

Actual endpoints currently defined in `api/`:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/documents/upload` | Upload `.txt` or `.md` document |
| `GET` | `/documents` | List documents |
| `GET` | `/documents/{document_id}/chunks` | List chunks for a document |
| `POST` | `/documents/{document_id}/supersede` | Mark a document superseded by another document |
| `POST` | `/documents/{document_id}/embed` | Embed chunks for a document |
| `POST` | `/search/vector` | Vector search |
| `POST` | `/search/keyword` | Keyword search |
| `POST` | `/search/hybrid` | Hybrid RRF search |
| `POST` | `/query` | Generate a verified answer with confidence/refusal fields |
| `POST` | `/query/debug` | Return query trace details |

Search endpoints accept `query`, `top_k`, `include_superseded`, and optional metadata filters such as `entity`, `document_type`, `document_date`, and `document_family_id`.

## End-to-End Workflow

1. Upload a document.
2. The document is stored and registered.
3. Text is parsed and chunked.
4. Chunks get contextualized embedding text.
5. Chunks are indexed for vector and keyword retrieval.
6. A user asks a question.
7. The engine retrieves evidence.
8. The engine builds source context.
9. The engine generates a cited answer.
10. The engine verifies claims and citations.
11. The engine scores confidence and refuses if evidence is weak.

## Running the Project

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

Default local URL:

```text
http://127.0.0.1:8000
```

## Running the Web UI

The web UI is a Vite React app under `frontend/`.

```powershell
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

The UI defaults to:

```text
VITE_RAG_API_BASE_URL=http://127.0.0.1:8000
```

Start the FastAPI backend first, then use the UI to check backend health, upload `.txt` or `.md` documents, list documents, view chunks, embed/index documents, ask questions, inspect citations, and view debug traces.

Build the web UI:

```powershell
cd frontend
npm run build
```

## Running the Desktop UI

The desktop app is a Tauri wrapper around the same React UI in `frontend/`. It does not contain a separate desktop UI.

Start the backend manually:

```powershell
python -m uvicorn app.main:app --reload
```

Run the desktop shell:

```powershell
cd frontend
npm run tauri:dev
```

Build the desktop shell when Rust and Tauri platform prerequisites are installed:

```powershell
cd frontend
npm run tauri:build
```

The desktop app connects to `http://127.0.0.1:8000` by default and shows the same backend offline state as the web UI when FastAPI is not running.

## Production Profile

LocalLite is still the default and complete runtime profile:

```text
STORAGE_PROFILE=local_lite
```

Production mode is prepared behind configuration:

```text
STORAGE_PROFILE=production
```

Production service configuration:

```powershell
docker compose -f docker-compose.production.yml config
```

Production environment template:

```text
.env.production.example
```

The production profile expects PostgreSQL, Qdrant, OpenSearch, and Redis. Adapter classes exist behind the storage factories, but they are skeletons until a future implementation completes real persistence and search behavior. See `docs/production.md`.

## Release Workflow

Local release commands:

```powershell
.\scripts\start_backend.ps1
.\scripts\start_web_ui.ps1
.\scripts\start_desktop_ui.ps1
.\scripts\verify_local_release.ps1
```

Use skips for CI-style validation when the backend is not already running or Tauri build scripts are blocked by local machine policy:

```powershell
.\scripts\verify_local_release.ps1 -SkipTauriBuild -SkipHealthCheck
```

Production config verification:

```powershell
.\scripts\verify_production_config.ps1
```

Release branches:

```text
release/desktop-local = LocalLite plus shared web UI and Tauri desktop packaging
release/online-prod = production Docker/server profile
```

`main` remains the shared source of truth. Release branches are targets, not separate products. See `docs/release.md` and `docs/BRANCHING_STRATEGY.md`.

## Running Tests

```powershell
python -m pytest -q
```

A Starlette/FastAPI `TestClient` deprecation warning may appear in the current dependency set; tests can still pass.

## Running Evaluation

Lightweight eval:

```powershell
python -m rag_engine.evals.lightweight_eval
```

Full eval:

```powershell
python -m rag_engine.evals.run_full_eval
```

Eval reports are written under:

```text
data/evals/results/
```

## Example Usage

Health check:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Upload a Markdown document:

```powershell
curl.exe -X POST http://127.0.0.1:8000/documents/upload `
  -F "file=@sample.md" `
  -F "entity=ExampleCo" `
  -F "document_type=policy"
```

Embed the uploaded document:

```powershell
curl.exe -X POST http://127.0.0.1:8000/documents/{document_id}/embed
```

Run hybrid search:

```powershell
curl.exe -X POST http://127.0.0.1:8000/search/hybrid `
  -H "Content-Type: application/json" `
  -d "{\"query\":\"risk factors\",\"top_k\":5}"
```

Ask a question:

```powershell
curl.exe -X POST http://127.0.0.1:8000/query `
  -H "Content-Type: application/json" `
  -d "{\"question\":\"What does the document say?\",\"top_k\":5}"
```

Inspect a debug trace:

```powershell
curl.exe -X POST http://127.0.0.1:8000/query/debug `
  -H "Content-Type: application/json" `
  -d "{\"question\":\"What does the document say?\",\"top_k\":5}"
```

## Repository Structure

```text
app/          FastAPI app setup, settings, dependencies, logging
api/          Route modules for health, documents, search, and query
frontend/     Shared Vite React UI
rag_engine/   Core ingestion, retrieval, generation, verification, eval, storage code
tests/        Unit and integration tests
docs/         Specifications, Codex slice prompts, and phase documentation
data/         Local raw files, processed SQLite data, and eval datasets/results
scripts/      Slice workflow, gate, and commit helper scripts
```

## Development Workflow

Development is slice-gated:

1. Each slice adds one vertical layer.
2. Tests are required for every slice.
3. The gate must pass before the next slice starts.
4. Each passing slice is committed separately.

Useful scripts:

```powershell
.\scripts\run_slice.ps1 -SliceId "slice-00" -SliceFile "docs/codex/slices/slice-00-project-foundation.md"
.\scripts\run_gate.ps1 -Slice "slice-00"
.\scripts\commit_slice.ps1 -Slice "slice-00" -Message "Slice 00: project foundation"
```

## Slice-Based Build History

| Slice | Purpose |
|---|---|
| 00 | Project foundation |
| 01 | Minimal document pipeline |
| 02 | Searchable vector retrieval |
| 03 | Grounded answers with citations |
| 04 | Lightweight eval and debug trace |
| 05 | Hybrid retrieval with RRF |
| 06 | Metadata filters and supersession |
| 07 | Reranker and evidence selector |
| 08 | Prompt-injection defense |
| 09 | Structured claims and citation verification |
| 10 | Confidence and refusal |
| 11 | Full evaluation harness |
| 12 | Production adapter interfaces |
| 13A | Shared web UI |
| 13B | Tauri desktop wrapper |
| 13C | Production backend adapter skeletons |
| 13D | Packaging and release workflow |

Detailed phase notes are in `docs/youtube/phase-00.md` through `docs/youtube/phase-13D.md`. The broader v3 specification is in `docs/spec/RAG_ENGINE_V3.md`.

## Roadmap

- Slice 13A: Shared Web UI
- Slice 13B: Tauri Desktop UI
- Slice 13C: Production database/vector/search adapters
- Slice 13D: Packaging and release
- Slice 14: Domain adapter specialization

## Known Limitations

- LocalLite mode is intended for local development and single-user use.
- Production adapters are skeletons, not full PostgreSQL, Qdrant, OpenSearch, or Redis implementations yet.
- The desktop release does not bundle the FastAPI backend as a sidecar yet.
- Local machine policy may block Tauri/Cargo build scripts.
- Quality depends on eval coverage.
- Large corpus aggregate questions may require a future map-reduce workflow.
- Local LLM behavior depends on the available local model.
- Current parsers support `.txt` and `.md`; richer document formats are future work.
- The default providers are deterministic test-friendly providers, not tuned production models.

## Why This Project Matters

This project demonstrates reliable AI system design, RAG architecture, evaluation-driven development, local-first privacy, source-grounded answer generation, and phase-gated engineering.

The important idea is that useful AI systems need more than a fluent model call. They need evidence retrieval, verification, refusal behavior, and traces that make answers inspectable.

## License

No license file is currently included. Add an explicit license before distributing or reusing this project outside its current private development context.
