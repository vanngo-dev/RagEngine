from fastapi import Depends

from app.config import Settings, get_settings
from rag_engine.generation.llm import LLMProvider, get_llm_provider
from rag_engine.retrieval.embeddings import EmbeddingProvider, get_embedding_provider
from rag_engine.retrieval.reranker import RerankerProvider, get_reranker_provider
from rag_engine.storage.factory import (
    get_document_store_for_profile,
    get_keyword_index_for_profile,
    get_vector_index_for_profile,
)
from rag_engine.storage.interfaces import DocumentStore, KeywordIndex, VectorIndex


def get_app_settings() -> Settings:
    return get_settings()


def get_document_store(
    settings: Settings = Depends(get_app_settings),
) -> DocumentStore:
    return get_document_store_for_profile(settings.storage_profile, settings.database_path)


def get_vector_index(
    settings: Settings = Depends(get_app_settings),
) -> VectorIndex:
    return get_vector_index_for_profile(settings.storage_profile, settings.database_path)


def get_keyword_index(
    settings: Settings = Depends(get_app_settings),
) -> KeywordIndex:
    return get_keyword_index_for_profile(settings.storage_profile, settings.database_path)


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
