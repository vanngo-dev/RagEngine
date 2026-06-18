# Codex Master Rules — Robust Local RAG Engine v3

You are coding a robust local-first RAG engine.

Follow these rules strictly:

1. Implement only the requested slice.
2. Do not build future slices early.
3. Do not skip tests.
4. Do not remove existing tests unless replacing them with better tests.
5. Keep the engine modular and interface-based.
6. Use LocalLite stack first:
   - FastAPI
   - SQLite
   - SQLite FTS5
   - LanceDB
   - Ollama-compatible LLM provider
   - Pytest
7. Do not add PostgreSQL, Qdrant, OpenSearch, Redis, or MinIO until the production adapter slice.
8. Every slice must update or create docs/youtube/phase-X.md.
9. Every slice must include tests.
10. Every slice must preserve existing behavior.
11. If a requirement is unclear, choose the simplest implementation that satisfies the acceptance criteria.
12. Do not do large unrelated refactors.
13. At the end of every slice, report:
    - files changed
    - tests added
    - tests run
    - manual validation commands
    - known limitations
    - recommended commit message
14. Stop after the requested slice.
15. Do not implement UI unless the slice explicitly asks for API contract work.
