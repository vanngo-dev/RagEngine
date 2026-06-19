from pathlib import Path

from rag_engine.storage.local_lite import (
    LocalLiteJobStore,
    create_local_lite_document_store,
    create_local_lite_keyword_index,
    create_local_lite_vector_index,
)
from rag_engine.storage.placeholders import (
    OpenSearchKeywordIndex,
    PostgresDocumentStore,
    QdrantVectorIndex,
    RedisJobStore,
)


def normalize_profile(profile: str) -> str:
    return profile.strip().lower()


def get_document_store_for_profile(profile: str, database_path: Path | str):
    normalized = normalize_profile(profile)
    if normalized == "local_lite":
        return create_local_lite_document_store(database_path)
    if normalized == "postgres":
        return PostgresDocumentStore()

    raise ValueError(f"Unknown document storage profile: {profile}")


def get_vector_index_for_profile(profile: str, database_path: Path | str):
    normalized = normalize_profile(profile)
    if normalized == "local_lite":
        return create_local_lite_vector_index(database_path)
    if normalized == "qdrant":
        return QdrantVectorIndex()

    raise ValueError(f"Unknown vector index profile: {profile}")


def get_keyword_index_for_profile(profile: str, database_path: Path | str):
    normalized = normalize_profile(profile)
    if normalized == "local_lite":
        return create_local_lite_keyword_index(database_path)
    if normalized == "opensearch":
        return OpenSearchKeywordIndex()

    raise ValueError(f"Unknown keyword index profile: {profile}")


def get_job_store_for_profile(profile: str):
    normalized = normalize_profile(profile)
    if normalized == "local_lite":
        return LocalLiteJobStore()
    if normalized == "redis_jobs":
        return RedisJobStore()

    raise ValueError(f"Unknown job storage profile: {profile}")
