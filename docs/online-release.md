# Online Production Release

## Target

`release/online-prod` is for the production Docker/server profile.

## Services

The production Compose stack includes:

- PostgreSQL on `5432`
- Qdrant on `6333` and `6334`
- OpenSearch on `9200` and `9600`
- Redis on `6379`

Volumes:

- `postgres_data`
- `qdrant_data`
- `opensearch_data`
- `redis_data`

## Verify Configuration

```powershell
.\scripts\verify_production_config.ps1
```

Equivalent Docker check:

```powershell
docker compose -f docker-compose.production.yml config
```

## Start Services

```powershell
docker compose -f docker-compose.production.yml up -d
```

## Known Limitations

- Production adapters are skeletons and do not yet implement full persistence/search behavior.
- No cloud deployment, TLS, auth, backups, migrations, or monitoring are included.
- Do not treat this branch as a separate app; source changes belong on `main`.
