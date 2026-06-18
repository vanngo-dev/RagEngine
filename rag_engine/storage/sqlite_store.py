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
            self._ensure_document_columns(connection)
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
            connection.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts
                USING fts5(
                    chunk_id UNINDEXED,
                    document_id UNINDEXED,
                    text
                )
                """
            )
            connection.commit()

    def _ensure_document_columns(self, connection: sqlite3.Connection) -> None:
        existing_columns = {
            row["name"]
            for row in connection.execute("PRAGMA table_info(documents)").fetchall()
        }
        columns = {
            "document_family_id": "TEXT",
            "entity": "TEXT",
            "document_type": "TEXT",
            "document_date": "TEXT",
            "superseded_by_document_id": "TEXT",
        }

        for column_name, column_type in columns.items():
            if column_name not in existing_columns:
                connection.execute(
                    f"ALTER TABLE documents ADD COLUMN {column_name} {column_type}"
                )

        connection.execute(
            "UPDATE documents SET document_family_id = id WHERE document_family_id IS NULL OR document_family_id = ''"
        )
        connection.execute(
            "UPDATE documents SET entity = '' WHERE entity IS NULL"
        )
        connection.execute(
            "UPDATE documents SET document_type = source_type WHERE document_type IS NULL OR document_type = ''"
        )
        connection.execute(
            "UPDATE documents SET document_date = '' WHERE document_date IS NULL"
        )

    def create_document(
        self,
        document_id: str,
        title: str,
        file_name: str,
        file_path: str,
        source_type: str,
        content_hash: str,
        status: str,
        document_family_id: str | None = None,
        entity: str = "",
        document_type: str | None = None,
        document_date: str = "",
    ) -> dict:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO documents (
                    id,
                    title,
                    file_name,
                    file_path,
                    source_type,
                    content_hash,
                    status,
                    document_family_id,
                    entity,
                    document_type,
                    document_date,
                    superseded_by_document_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
                """,
                (
                    document_id,
                    title,
                    file_name,
                    file_path,
                    source_type,
                    content_hash,
                    status,
                    document_family_id or document_id,
                    entity,
                    document_type or source_type,
                    document_date,
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
            connection.executemany(
                """
                INSERT INTO chunk_fts (chunk_id, document_id, text)
                VALUES (?, ?, ?)
                """,
                [
                    (
                        chunk["chunk_id"],
                        chunk["document_id"],
                        chunk["text"],
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

    def supersede_document(
        self,
        old_document_id: str,
        new_document_id: str,
    ) -> dict:
        old_document = self.get_document(old_document_id)
        if old_document is None:
            raise ValueError("Document to supersede was not found")

        new_document = self.get_document(new_document_id)
        if new_document is None:
            raise ValueError("Replacement document was not found")

        family_id = old_document.get("document_family_id") or old_document_id
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE documents
                SET
                    status = 'superseded',
                    superseded_by_document_id = ?,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                WHERE id = ?
                """,
                (new_document_id, old_document_id),
            )
            connection.execute(
                """
                UPDATE documents
                SET
                    status = 'active',
                    document_family_id = ?,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                WHERE id = ?
                """,
                (family_id, new_document_id),
            )
            connection.commit()

        return {
            "superseded_document": self.get_document(old_document_id),
            "active_document": self.get_document(new_document_id),
        }
