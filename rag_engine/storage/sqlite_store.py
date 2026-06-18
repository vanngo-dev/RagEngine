import sqlite3
from pathlib import Path
from typing import Iterable


def utc_now_sql() -> str:
    return "strftime('%Y-%m-%dT%H:%M:%fZ', 'now')"


class SQLiteDocumentStore:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    content_hash TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    text TEXT NOT NULL,
                    embedding_text TEXT NOT NULL,
                    section_title TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    token_count INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                    FOREIGN KEY (document_id) REFERENCES documents(id)
                )
                """
            )
            connection.commit()

    def create_document(
        self,
        document_id: str,
        title: str,
        file_name: str,
        file_path: str,
        source_type: str,
        content_hash: str,
        status: str,
    ) -> dict:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO documents (
                    id, title, file_name, file_path, source_type, content_hash, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    title,
                    file_name,
                    file_path,
                    source_type,
                    content_hash,
                    status,
                ),
            )
            connection.commit()

        document = self.get_document(document_id)
        if document is None:
            raise RuntimeError("Document was not persisted")
        return document

    def create_chunks(self, chunks: Iterable[dict]) -> None:
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO chunks (
                    chunk_id,
                    document_id,
                    text,
                    embedding_text,
                    section_title,
                    chunk_index,
                    token_count
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        chunk["chunk_id"],
                        chunk["document_id"],
                        chunk["text"],
                        chunk["embedding_text"],
                        chunk["section_title"],
                        chunk["chunk_index"],
                        chunk["token_count"],
                    )
                    for chunk in chunks
                ],
            )
            connection.commit()

    def get_document(self, document_id: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE id = ?",
                (document_id,),
            ).fetchone()

        return dict(row) if row else None

    def get_document_by_hash(self, digest: str) -> dict | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM documents WHERE content_hash = ?",
                (digest,),
            ).fetchone()

        return dict(row) if row else None

    def list_documents(self) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM documents ORDER BY created_at, id"
            ).fetchall()

        return [dict(row) for row in rows]

    def list_chunks(self, document_id: str) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM chunks
                WHERE document_id = ?
                ORDER BY chunk_index
                """,
                (document_id,),
            ).fetchall()

        return [dict(row) for row in rows]
