from rag_engine.retrieval.indexing import embed_document
from rag_engine.retrieval.vector_index import SQLiteVectorIndex
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


class CapturingEmbeddingProvider:
    def __init__(self) -> None:
        self.texts: list[str] = []

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        self.texts = texts
        return [[1.0, 0.0] for _ in texts]

    def embed_text(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]


def test_embedding_uses_embedding_text(tmp_path) -> None:
    database_path = tmp_path / "rag.sqlite3"
    store = SQLiteDocumentStore(database_path)
    store.create_document(
        document_id="doc_test",
        title="Policy",
        file_name="policy.md",
        file_path="policy.md",
        source_type="md",
        content_hash="hash",
        status="uploaded",
    )
    store.create_chunks(
        [
            {
                "chunk_id": "chunk_policy",
                "document_id": "doc_test",
                "text": "Raw text only.",
                "embedding_text": "Document: Policy\nDocument Type: md\nSection: Intro\n\nRaw text only.",
                "section_title": "Intro",
                "chunk_index": 0,
                "token_count": 3,
            }
        ]
    )

    provider = CapturingEmbeddingProvider()
    embedded = embed_document(
        document_id="doc_test",
        store=store,
        vector_index=SQLiteVectorIndex(database_path),
        embedding_provider=provider,
    )

    assert embedded == 1
    assert provider.texts == [
        "Document: Policy\nDocument Type: md\nSection: Intro\n\nRaw text only."
    ]
