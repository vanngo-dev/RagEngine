from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.config import Settings
from app.dependencies import (
    get_app_embedding_provider,
    get_app_llm_provider,
    get_app_reranker_provider,
    get_app_settings,
)
from rag_engine.generation.llm import LLMProvider
from rag_engine.generation.query import answer_question, debug_question
from rag_engine.retrieval.embeddings import EmbeddingProvider
from rag_engine.retrieval.keyword_index import SQLiteKeywordIndex
from rag_engine.retrieval.reranker import RerankerProvider
from rag_engine.retrieval.vector_index import SQLiteVectorIndex
from rag_engine.storage.factory import (
    get_keyword_index_for_profile,
    get_vector_index_for_profile,
)


router = APIRouter(tags=["query"])


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


def get_vector_index(settings: Settings = Depends(get_app_settings)) -> SQLiteVectorIndex:
    return get_vector_index_for_profile(settings.storage_profile, settings.database_path)


def get_keyword_index(settings: Settings = Depends(get_app_settings)) -> SQLiteKeywordIndex:
    return get_keyword_index_for_profile(settings.storage_profile, settings.database_path)


@router.post("/query")
def query(
    request: QueryRequest,
    vector_index: SQLiteVectorIndex = Depends(get_vector_index),
    keyword_index: SQLiteKeywordIndex = Depends(get_keyword_index),
    embedding_provider: EmbeddingProvider = Depends(get_app_embedding_provider),
    llm_provider: LLMProvider = Depends(get_app_llm_provider),
    reranker_provider: RerankerProvider = Depends(get_app_reranker_provider),
) -> dict:
    return answer_question(
        question=request.question,
        vector_index=vector_index,
        keyword_index=keyword_index,
        embedding_provider=embedding_provider,
        llm_provider=llm_provider,
        reranker_provider=reranker_provider,
        top_k=request.top_k,
    )


@router.post("/query/debug")
def query_debug(
    request: QueryRequest,
    vector_index: SQLiteVectorIndex = Depends(get_vector_index),
    keyword_index: SQLiteKeywordIndex = Depends(get_keyword_index),
    embedding_provider: EmbeddingProvider = Depends(get_app_embedding_provider),
    llm_provider: LLMProvider = Depends(get_app_llm_provider),
    reranker_provider: RerankerProvider = Depends(get_app_reranker_provider),
) -> dict:
    return debug_question(
        question=request.question,
        vector_index=vector_index,
        keyword_index=keyword_index,
        embedding_provider=embedding_provider,
        llm_provider=llm_provider,
        reranker_provider=reranker_provider,
        top_k=request.top_k,
    )
