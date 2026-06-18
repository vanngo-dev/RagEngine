from rag_engine.evals.lightweight_eval import recall_at_k
from rag_engine.retrieval.embeddings import FakeEmbeddingProvider
from rag_engine.retrieval.vector_index import SQLiteVectorIndex
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


def test_fake_embedding_provider_returns_stable_vectors() -> None:
    provider = FakeEmbeddingProvider()

    first = provider.embed_text("risk factors")
    second = provider.embed_text("risk factors")

    assert first == second
    assert len(first) == 64


def test_vector_index_stores_chunks_and_search_returns_metadata(tmp_path) -> None:
    database_path = tmp_path / "rag.sqlite3"
    store = SQLiteDocumentStore(database_path)
    document = store.create_document(
        document_id="doc_test",
        title="Risk Memo",
        file_name="risk.md",
        file_path="risk.md",
        source_type="md",
        content_hash="hash",
        status="uploaded",
    )
    store.create_chunks(
        [
            {
                "chunk_id": "chunk_risk",
                "document_id": document["id"],
                "text": "Risk factors include supply chain delays.",
                "embedding_text": "Document: Risk Memo\nDocument Type: md\nSection: Risk\n\nRisk factors include supply chain delays.",
                "section_title": "Risk",
                "chunk_index": 0,
                "token_count": 6,
            }
        ]
    )

    provider = FakeEmbeddingProvider()
    index = SQLiteVectorIndex(database_path)
    index.upsert_vector(
        chunk_id="chunk_risk",
        document_id="doc_test",
        section_title="Risk",
        status="uploaded",
        vector=provider.embed_text("Risk factors include supply chain delays."),
    )

    results = index.search(provider.embed_text("risk factors"), top_k=1)

    assert index.count_vectors() == 1
    assert results[0]["chunk_id"] == "chunk_risk"
    assert results[0]["text"] == "Risk factors include supply chain delays."
    assert results[0]["metadata"]["document_id"] == "doc_test"
    assert results[0]["metadata"]["section_title"] == "Risk"
    assert results[0]["metadata"]["status"] == "uploaded"


def test_recall_at_k_calculation() -> None:
    assert recall_at_k(["a", "b", "c"], ["b"], 2) == 1.0
    assert recall_at_k(["a", "b", "c"], ["c"], 2) == 0.0
