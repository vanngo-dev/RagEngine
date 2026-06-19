from pathlib import Path
from uuid import uuid4

from rag_engine.retrieval.keyword_index import SQLiteKeywordIndex
from rag_engine.retrieval.vector_index import SQLiteVectorIndex
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


class LocalLiteJobStore:
    def __init__(self) -> None:
        self.jobs: dict[str, dict] = {}

    def create_job(self, job_type: str, payload: dict) -> dict:
        job = {
            "job_id": f"job_{uuid4().hex}",
            "job_type": job_type,
            "payload": payload,
            "status": "created",
        }
        self.jobs[job["job_id"]] = job
        return job


def create_local_lite_document_store(database_path: Path | str) -> SQLiteDocumentStore:
    return SQLiteDocumentStore(database_path)


def create_local_lite_vector_index(database_path: Path | str) -> SQLiteVectorIndex:
    return SQLiteVectorIndex(database_path)


def create_local_lite_keyword_index(database_path: Path | str) -> SQLiteKeywordIndex:
    return SQLiteKeywordIndex(database_path)
