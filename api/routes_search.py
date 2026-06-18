from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.dependencies import get_app_embedding_provider, get_app_settings
from app.config import Settings
from rag_engine.retrieval.embeddings import EmbeddingProvider
from rag_engine.retrieval.vector_index import SQLiteVectorIndex


router = APIRouter(prefix="/search", tags=["search"])


class VectorSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)


def get_vector_index(settings: Settings = Depends(get_app_settings)) -> SQLiteVectorIndex:
    return SQLiteVectorIndex(settings.database_path)


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
        "results": vector_index.search(query_vector, top_k=request.top_k),
    }
