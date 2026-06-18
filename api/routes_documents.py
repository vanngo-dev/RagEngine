from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.config import Settings
from app.dependencies import get_app_embedding_provider, get_app_settings
from rag_engine.ingestion.pipeline import ingest_upload
from rag_engine.retrieval.embeddings import EmbeddingProvider
from rag_engine.retrieval.indexing import embed_document
from rag_engine.retrieval.vector_index import SQLiteVectorIndex
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


router = APIRouter(prefix="/documents", tags=["documents"])


def get_store(settings: Settings = Depends(get_app_settings)) -> SQLiteDocumentStore:
    return SQLiteDocumentStore(settings.database_path)


def get_vector_index(settings: Settings = Depends(get_app_settings)) -> SQLiteVectorIndex:
    return SQLiteVectorIndex(settings.database_path)


@router.post("/upload")
async def upload_document(
    file: UploadFile,
    settings: Settings = Depends(get_app_settings),
    store: SQLiteDocumentStore = Depends(get_store),
) -> dict:
    try:
        result = await ingest_upload(file, settings, store)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return result


@router.get("")
def list_documents(store: SQLiteDocumentStore = Depends(get_store)) -> dict:
    return {"documents": store.list_documents()}


@router.get("/{document_id}/chunks")
def list_document_chunks(
    document_id: str,
    store: SQLiteDocumentStore = Depends(get_store),
) -> dict:
    if store.get_document(document_id) is None:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"chunks": store.list_chunks(document_id)}


@router.post("/{document_id}/embed")
def embed_document_chunks(
    document_id: str,
    store: SQLiteDocumentStore = Depends(get_store),
    vector_index: SQLiteVectorIndex = Depends(get_vector_index),
    embedding_provider: EmbeddingProvider = Depends(get_app_embedding_provider),
) -> dict:
    try:
        embedded_chunks = embed_document(
            document_id=document_id,
            store=store,
            vector_index=vector_index,
            embedding_provider=embedding_provider,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "document_id": document_id,
        "embedded_chunks": embedded_chunks,
    }
