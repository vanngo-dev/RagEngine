import importlib.util
from dataclasses import dataclass


class MissingProductionDependencyError(RuntimeError):
    """Raised when a production adapter is selected without its optional package."""


@dataclass(frozen=True)
class ProductionAdapterConfig:
    adapter_name: str
    dependency_module: str
    install_hint: str


class ProductionAdapterSkeleton:
    adapter_config = ProductionAdapterConfig(
        adapter_name="production",
        dependency_module="",
        install_hint="Install the production adapter dependencies.",
    )

    def __init__(self, **config) -> None:
        self.config = config
        self._require_dependency()
        raise NotImplementedError(
            f"{self.adapter_config.adapter_name} adapter is a production skeleton and is not fully implemented yet. "
            "Use STORAGE_PROFILE=local_lite until the production adapter is completed."
        )

    def _require_dependency(self) -> None:
        dependency_module = self.adapter_config.dependency_module
        if not dependency_module:
            return

        if importlib.util.find_spec(dependency_module) is None:
            raise MissingProductionDependencyError(
                f"{self.adapter_config.adapter_name} requires optional dependency "
                f"'{dependency_module}'. {self.adapter_config.install_hint}"
            )


class PostgresDocumentStore(ProductionAdapterSkeleton):
    adapter_config = ProductionAdapterConfig(
        adapter_name="PostgreSQL document store",
        dependency_module="psycopg",
        install_hint="Install psycopg before using STORAGE_PROFILE=production.",
    )


class PostgresChunkStore(ProductionAdapterSkeleton):
    adapter_config = ProductionAdapterConfig(
        adapter_name="PostgreSQL chunk store",
        dependency_module="psycopg",
        install_hint="Install psycopg before using STORAGE_PROFILE=production.",
    )


class QdrantVectorIndex(ProductionAdapterSkeleton):
    adapter_config = ProductionAdapterConfig(
        adapter_name="Qdrant vector index",
        dependency_module="qdrant_client",
        install_hint="Install qdrant-client before using STORAGE_PROFILE=production.",
    )


class OpenSearchKeywordIndex(ProductionAdapterSkeleton):
    adapter_config = ProductionAdapterConfig(
        adapter_name="OpenSearch keyword index",
        dependency_module="opensearchpy",
        install_hint="Install opensearch-py before using STORAGE_PROFILE=production.",
    )


class RedisJobStore(ProductionAdapterSkeleton):
    adapter_config = ProductionAdapterConfig(
        adapter_name="Redis job store",
        dependency_module="redis",
        install_hint="Install redis before using STORAGE_PROFILE=production.",
    )
