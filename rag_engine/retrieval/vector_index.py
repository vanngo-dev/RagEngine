import json
import math
import sqlite3
from pathlib import Path


class SQLiteVectorIndex:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        from rag_engine.storage.sqlite_store import SQLiteDocumentStore

        SQLiteDocumentStore(self.database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS vector_embeddings (
                    chunk_id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    section_title TEXT NOT NULL,
                    status TEXT NOT NULL,
                    vector_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
                    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
                )
                """
            )
            connection.commit()

    def upsert_vector(
        self,
        chunk_id: str,
        document_id: str,
        section_title: str,
        status: str,
        vector: list[float],
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO vector_embeddings (
                    chunk_id, document_id, section_title, status, vector_json
                )
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(chunk_id) DO UPDATE SET
                    document_id = excluded.document_id,
                    section_title = excluded.section_title,
                    status = excluded.status,
                    vector_json = excluded.vector_json,
                    updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                """,
                (
                    chunk_id,
                    document_id,
                    section_title,
                    status,
                    json.dumps(vector),
                ),
            )
            connection.commit()

    def count_vectors(self) -> int:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM vector_embeddings"
            ).fetchone()

        return int(row["total"])

    def search(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    ve.chunk_id,
                    ve.document_id,
                    ve.section_title,
                    ve.status,
                    ve.vector_json,
                    c.text,
                    c.chunk_index,
                    c.token_count
                FROM vector_embeddings ve
                JOIN chunks c ON c.chunk_id = ve.chunk_id
                ORDER BY ve.updated_at DESC, ve.chunk_id
                """
            ).fetchall()

        scored = []
        for row in rows:
            vector = json.loads(row["vector_json"])
            score = cosine_similarity(query_vector, vector)
            scored.append(
                {
                    "chunk_id": row["chunk_id"],
                    "document_id": row["document_id"],
                    "text": row["text"],
                    "score": score,
                    "metadata": {
                        "chunk_id": row["chunk_id"],
                        "document_id": row["document_id"],
                        "section_title": row["section_title"],
                        "status": row["status"],
                        "chunk_index": row["chunk_index"],
                        "token_count": row["token_count"],
                    },
                }
            )

        scored.sort(key=lambda item: (-item["score"], item["chunk_id"]))
        return scored[:top_k]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0

    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))

    if left_norm == 0 or right_norm == 0:
        return 0.0

    return numerator / (left_norm * right_norm)
