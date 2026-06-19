# Production Profile

## Status

The production profile is prepared behind configuration, but it is not a complete production implementation yet.

LocalLite remains the default:

```text
STORAGE_PROFILE=local_lite
```

The production profile is selected with:

```text
STORAGE_PROFILE=production
```

## Production Services

`docker-compose.production.yml` defines the external services expected by the production profile:

- PostgreSQL for document metadata and chunks
- Qdrant for vector search
- OpenSearch for keyword search
- Redis for job state or queue-backed work

Validate the Compose file:

```powershell
docker compose -f docker-compose.production.yml config
```

## Adapter Skeletons

The codebase includes these production adapter skeletons:

- `PostgresDocumentStore`
- `PostgresChunkStore`
- `QdrantVectorIndex`
- `OpenSearchKeywordIndex`
- `RedisJobStore`

The skeletons sit behind the existing storage factory layer. They do not load during LocalLite tests.

If `STORAGE_PROFILE=production` is selected without optional production dependencies, the app raises a clear dependency error. This is intentional; the current slice prepares the adapter boundaries and service configuration without pretending full production storage is complete.

## Environment

Copy `.env.production.example` to a deployment-specific environment file and adjust:

```text
POSTGRES_DSN
QDRANT_URL
QDRANT_COLLECTION
OPENSEARCH_URL
OPENSEARCH_INDEX
REDIS_URL
CORS_ALLOWED_ORIGINS
```

## Optional Python Packages

The production skeletons name these optional packages:

```text
psycopg
qdrant-client
opensearch-py
redis
```

Do not add these to the LocalLite default path unless a future slice implements and validates the real adapters.

## Known Limitations

- Production adapter classes are skeletons, not full database/search/vector implementations.
- No cloud deployment, auth, TLS, backup, migration, or observability stack is included.
- LocalLite remains the only fully working storage profile in this repository state.
