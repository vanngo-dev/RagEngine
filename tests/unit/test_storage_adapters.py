import pytest

from app.config import Settings
from rag_engine.interfaces import (
    CitationVerifier,
    ChunkStore,
    DocumentStore,
    EmbeddingProvider,
    JobStore,
    KeywordIndex,
    LLMProvider,
    RerankerProvider,
    VectorIndex,
)
from rag_engine.storage.factory import (
    get_chunk_store_for_profile,
    get_document_store_for_profile,
    get_job_store_for_profile,
    get_keyword_index_for_profile,
    get_vector_index_for_profile,
)
from rag_engine.storage.placeholders import (
    MissingProductionDependencyError,
    OpenSearchKeywordIndex,
    PostgresChunkStore,
    PostgresDocumentStore,
    QdrantVectorIndex,
    RedisJobStore,
)


def test_storage_profile_loads_default_local_lite() -> None:
    assert Settings().storage_profile == "local_lite"


def test_production_profile_config_loads() -> None:
    settings = Settings(
        storage_profile="production",
        postgres_dsn="postgresql://rag:rag@postgres:5432/rag_engine",
        qdrant_url="http://qdrant:6333",
        opensearch_url="http://opensearch:9200",
        redis_url="redis://redis:6379/0",
    )

    assert settings.storage_profile == "production"
    assert settings.postgres_dsn.startswith("postgresql://")
    assert settings.qdrant_url == "http://qdrant:6333"
    assert settings.opensearch_url == "http://opensearch:9200"
    assert settings.redis_url == "redis://redis:6379/0"


def test_local_lite_still_works_through_interfaces(tmp_path) -> None:
    store = get_document_store_for_profile("local_lite", tmp_path / "rag.sqlite3")
    document = store.create_document(
        document_id="doc_interface",
        title="Interface",
        file_name="interface.md",
        file_path="interface.md",
        source_type="md",
        content_hash="interface_hash",
        status="active",
    )

    assert document["id"] == "doc_interface"
    assert store.get_document("doc_interface")["title"] == "Interface"


def test_production_adapter_classes_exist() -> None:
    assert PostgresDocumentStore
    assert PostgresChunkStore
    assert QdrantVectorIndex
    assert OpenSearchKeywordIndex
    assert RedisJobStore


def test_missing_production_dependency_gives_clear_error(monkeypatch) -> None:
    monkeypatch.setattr(
        "rag_engine.storage.placeholders.importlib.util.find_spec",
        lambda name: None,
    )

    with pytest.raises(MissingProductionDependencyError, match="psycopg"):
        PostgresDocumentStore()


def test_production_profile_routes_to_adapter_skeletons(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(
        "rag_engine.storage.placeholders.importlib.util.find_spec",
        lambda name: None,
    )

    with pytest.raises(MissingProductionDependencyError, match="PostgreSQL document store"):
        get_document_store_for_profile("production", tmp_path / "rag.sqlite3")

    with pytest.raises(MissingProductionDependencyError, match="PostgreSQL chunk store"):
        get_chunk_store_for_profile("production", tmp_path / "rag.sqlite3")

    with pytest.raises(MissingProductionDependencyError, match="Qdrant vector index"):
        get_vector_index_for_profile("production", tmp_path / "rag.sqlite3")

    with pytest.raises(MissingProductionDependencyError, match="OpenSearch keyword index"):
        get_keyword_index_for_profile("production", tmp_path / "rag.sqlite3")

    with pytest.raises(MissingProductionDependencyError, match="Redis job store"):
        get_job_store_for_profile("production")


def test_required_interface_names_exist() -> None:
    assert DocumentStore
    assert ChunkStore
    assert VectorIndex
    assert KeywordIndex
    assert JobStore
    assert EmbeddingProvider
    assert LLMProvider
    assert RerankerProvider
    assert CitationVerifier
