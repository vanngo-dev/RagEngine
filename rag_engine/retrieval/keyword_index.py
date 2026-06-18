import re
import sqlite3
from pathlib import Path

from rag_engine.storage.sqlite_store import SQLiteDocumentStore


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9]+")


class SQLiteKeywordIndex:
    def __init__(self, database_path: Path | str) -> None:
        self.database_path = Path(database_path)
        SQLiteDocumentStore(self.database_path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        fts_query = normalize_fts_query(query)
        if not fts_query:
            return []

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    f.chunk_id,
                    f.document_id,
                    c.text,
                    c.section_title,
                    c.chunk_index,
                    c.token_count,
                    d.status,
                    bm25(chunk_fts) AS rank
                FROM chunk_fts f
                JOIN chunks c ON c.chunk_id = f.chunk_id
                JOIN documents d ON d.id = f.document_id
                WHERE chunk_fts MATCH ?
                ORDER BY rank, f.chunk_id
                LIMIT ?
                """,
                (fts_query, top_k),
            ).fetchall()

        results = []
        for row in rows:
            score = -float(row["rank"])
            results.append(
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

        return results


def normalize_fts_query(query: str) -> str:
    stripped = query.strip()
    if not stripped:
        return ""

    if stripped.startswith('"') and stripped.endswith('"'):
        return stripped

    tokens = TOKEN_PATTERN.findall(stripped)
    return " ".join(tokens)
