import hashlib
import re
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import Settings
from rag_engine.ingestion.chunker import build_embedding_text, chunk_blocks
from rag_engine.ingestion.parsers import parse_document, validate_supported_file
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


SAFE_FILE_PATTERN = re.compile(r"[^A-Za-z0-9._-]+")


def content_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def safe_file_name(file_name: str) -> str:
    name = Path(file_name).name.strip()
    sanitized = SAFE_FILE_PATTERN.sub("_", name)
    return sanitized or "uploaded_document"


async def ingest_upload(
    file: UploadFile,
    settings: Settings,
    store: SQLiteDocumentStore,
    entity: str | None = None,
    document_type: str | None = None,
    document_date: str | None = None,
    document_family_id: str | None = None,
) -> dict:
    file_name = safe_file_name(file.filename or "uploaded_document")
    source_type = validate_supported_file(file_name)
    content = await file.read()

    if not content:
        raise ValueError("Uploaded file is empty")

    digest = content_hash(content)
    existing = store.get_document_by_hash(digest)
    if existing is not None:
        return {"duplicate": True, "document": existing}

    document_id = f"doc_{uuid4().hex}"
    title = Path(file_name).stem or file_name
    document_dir = settings.raw_data_dir / document_id
    document_dir.mkdir(parents=True, exist_ok=True)
    file_path = document_dir / file_name
    file_path.write_bytes(content)

    document = store.create_document(
        document_id=document_id,
        title=title,
        file_name=file_name,
        file_path=str(file_path),
        source_type=source_type,
        content_hash=digest,
        status="active",
        document_family_id=document_family_id or document_id,
        entity=entity or "",
        document_type=document_type or source_type,
        document_date=document_date or "",
    )

    blocks = parse_document(file_name, content)
    chunks = chunk_blocks(blocks, settings.chunk_max_tokens)
    chunk_records = []

    for chunk in chunks:
        embedding_text = build_embedding_text(
            title=document["title"],
            source_type=document["source_type"],
            section_title=chunk.section_title,
            text=chunk.text,
        )
        chunk_records.append(
            {
                "chunk_id": f"{document_id}_chunk_{chunk.chunk_index:04d}",
                "document_id": document_id,
                "text": chunk.text,
                "embedding_text": embedding_text,
                "section_title": chunk.section_title,
                "chunk_index": chunk.chunk_index,
                "token_count": chunk.token_count,
            }
        )

    store.create_chunks(chunk_records)

    return {
        "duplicate": False,
        "document": document,
        "chunks_created": len(chunk_records),
    }
