from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.config import Settings
from app.dependencies import (
    get_app_embedding_provider,
    get_app_settings,
)
from rag_engine.retrieval.embeddings import EmbeddingProvider
from rag_engine.retrieval.hybrid import hybrid_search
from rag_engine.retrieval.keyword_index import SQLiteKeywordIndex
from rag_engine.retrieval.vector_index import SQLiteVectorIndex


router = APIRouter(prefix="/search", tags=["search"])


class VectorSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    include_superseded: bool = False
    document_family_id: str | None = None
    entity: str | None = None
    document_type: str | None = None
    document_date: str | None = None

    def metadata_filters(self) -> dict[str, str]:
        filters = {}
        for key in (
            "document_family_id",
            "entity",
            "document_type",
            "document_date",
        ):
            value = getattr(self, key)
            if value:
                filters[key] = value
        return filters


def get_vector_index(settings: Settings = Depends(get_app_settings)) -> SQLiteVectorIndex:
    return SQLiteVectorIndex(settings.database_path)


def get_keyword_index(settings: Settings = Depends(get_app_settings)) -> SQLiteKeywordIndex:
    return SQLiteKeywordIndex(settings.database_path)


@router.post("/vector")
def vector_search(
    request: VectorSearchRequest,
    vector_index: SQLiteVectorIndex = Depends(get_vector_index),
    embedding_provider: EmbeddingProvider = Depends(get_app_embedding_provider),
) -> dict:
    query_vector = embedding_provider.embed_text(request.query)
    return {
        "query": request.query,
        "top_k": request.top_k,
        "results": vector_index.search(
            query_vector,
            top_k=request.top_k,
            include_superseded=request.include_superseded,
            filters=request.metadata_filters(),
        ),
    }


@router.post("/keyword")
def keyword_search(
    request: VectorSearchRequest,
    keyword_index: SQLiteKeywordIndex = Depends(get_keyword_index),
) -> dict:
    return {
        "query": request.query,
        "top_k": request.top_k,
        "results": keyword_index.search(
            request.query,
            top_k=request.top_k,
            include_superseded=request.include_superseded,
            filters=request.metadata_filters(),
        ),
    }


@router.post("/hybrid")
def hybrid_search_endpoint(
    request: VectorSearchRequest,
    vector_index: SQLiteVectorIndex = Depends(get_vector_index),
    keyword_index: SQLiteKeywordIndex = Depends(get_keyword_index),
    embedding_provider: EmbeddingProvider = Depends(get_app_embedding_provider),
) -> dict:
    return {
        "query": request.query,
        "top_k": request.top_k,
        "results": hybrid_search(
            query=request.query,
            top_k=request.top_k,
            vector_index=vector_index,
            keyword_index=keyword_index,
            embedding_provider=embedding_provider,
            include_superseded=request.include_superseded,
            filters=request.metadata_filters(),
        ),
    }
