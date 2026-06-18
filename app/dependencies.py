from fastapi import Depends

from app.config import Settings, get_settings
from rag_engine.generation.llm import LLMProvider, get_llm_provider
from rag_engine.retrieval.embeddings import EmbeddingProvider, get_embedding_provider
from rag_engine.retrieval.keyword_index import SQLiteKeywordIndex
from rag_engine.retrieval.reranker import RerankerProvider, get_reranker_provider
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


def get_keyword_index(
    settings: Settings = Depends(get_app_settings),
) -> SQLiteKeywordIndex:
    return SQLiteKeywordIndex(settings.database_path)


def get_app_embedding_provider(
    settings: Settings = Depends(get_app_settings),
) -> EmbeddingProvider:
    return get_embedding_provider(settings.embedding_provider)


def get_app_llm_provider(
    settings: Settings = Depends(get_app_settings),
) -> LLMProvider:
    return get_llm_provider(
        name=settings.llm_provider,
        ollama_base_url=settings.ollama_base_url,
        ollama_model=settings.ollama_model,
    )


def get_app_reranker_provider(
    settings: Settings = Depends(get_app_settings),
) -> RerankerProvider:
    return get_reranker_provider(settings.reranker_provider)
