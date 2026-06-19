# Phase 13C — Production Backend Adapters

## Video Goal

Prepare a production backend profile while preserving LocalLite as the default working mode.

## What Changed

- Added `STORAGE_PROFILE=production`.
- Added production configuration fields for PostgreSQL, Qdrant, OpenSearch, and Redis.
- Added production adapter skeleton classes:
  - `PostgresDocumentStore`
  - `PostgresChunkStore`
  - `QdrantVectorIndex`
  - `OpenSearchKeywordIndex`
  - `RedisJobStore`
- Added a production Docker Compose service stack.
- Added `.env.production.example`.
- Added `docs/production.md`.
- Added tests proving LocalLite remains default and production dependencies do not load during LocalLite operation.

## Validation

```powershell
python -m pytest -q
```

Production Compose validation when Docker is available:

```powershell
docker compose -f docker-compose.production.yml config
```

## Honest Status

This slice does not fake working production storage. The production classes are adapter skeletons that fail clearly if selected without optional dependencies or before full implementation.

## Known Limitations

- PostgreSQL, Qdrant, OpenSearch, and Redis adapters are not fully implemented yet.
- LocalLite is still the only complete runtime profile.
- Production auth, TLS, migrations, backup, and monitoring remain future work.
