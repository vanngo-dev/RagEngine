from app.config import Settings, get_settings
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


def get_app_settings() -> Settings:
    return get_settings()


def get_document_store() -> SQLiteDocumentStore:
    settings = get_settings()
    return SQLiteDocumentStore(settings.database_path)
