class UnimplementedProductionAdapter:
    adapter_name = "production"

    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            f"{self.adapter_name} adapter is a placeholder and has not been implemented. Use STORAGE_PROFILE=local_lite."
        )


class PostgresDocumentStore(UnimplementedProductionAdapter):
    adapter_name = "postgres"


class QdrantVectorIndex(UnimplementedProductionAdapter):
    adapter_name = "qdrant"


class OpenSearchKeywordIndex(UnimplementedProductionAdapter):
    adapter_name = "opensearch"


class RedisJobStore(UnimplementedProductionAdapter):
    adapter_name = "redis_jobs"
