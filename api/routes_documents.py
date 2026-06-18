from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from pydantic import BaseModel

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
    entity: str | None = Form(default=None),
    document_type: str | None = Form(default=None),
    document_date: str | None = Form(default=None),
    document_family_id: str | None = Form(default=None),
    settings: Settings = Depends(get_app_settings),
    store: SQLiteDocumentStore = Depends(get_store),
) -> dict:
    try:
        result = await ingest_upload(
            file=file,
            settings=settings,
            store=store,
            entity=entity,
            document_type=document_type,
            document_date=document_date,
            document_family_id=document_family_id,
        )
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


class SupersedeRequest(BaseModel):
    new_document_id: str


@router.post("/{document_id}/supersede")
def supersede_document(
    document_id: str,
    request: SupersedeRequest,
    store: SQLiteDocumentStore = Depends(get_store),
) -> dict:
    try:
        return store.supersede_document(
            old_document_id=document_id,
            new_document_id=request.new_document_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


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
