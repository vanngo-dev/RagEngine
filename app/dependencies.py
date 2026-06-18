from fastapi import Depends

from app.config import Settings, get_settings
from rag_engine.retrieval.embeddings import EmbeddingProvider, get_embedding_provider
from rag_engine.retrieval.vector_index import SQLiteVectorIndex
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


def get_app_settings() -> Settings:
    return get_settings()


def get_document_store(
    settings: Settings = Depends(get_app_settings),
) -> SQLiteDocumentStore:
    return SQLiteDocumentStore(settings.database_path)


def get_vector_index(
    settings: Settings = Depends(get_app_settings),
) -> SQLiteVectorIndex:
    return SQLiteVectorIndex(settings.database_path)


def get_app_embedding_provider(
    settings: Settings = Depends(get_app_settings),
) -> EmbeddingProvider:
    return get_embedding_provider(settings.embedding_provider)
