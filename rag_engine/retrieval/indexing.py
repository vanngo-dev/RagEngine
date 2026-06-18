from rag_engine.retrieval.embeddings import EmbeddingProvider
from rag_engine.retrieval.vector_index import SQLiteVectorIndex
from rag_engine.storage.sqlite_store import SQLiteDocumentStore


def embed_document(
    document_id: str,
    store: SQLiteDocumentStore,
    vector_index: SQLiteVectorIndex,
    embedding_provider: EmbeddingProvider,
) -> int:
    document = store.get_document(document_id)
    if document is None:
        raise ValueError("Document not found")

    chunks = store.list_chunks(document_id)
    texts_to_embed = [chunk["embedding_text"] for chunk in chunks]
    vectors = embedding_provider.embed_texts(texts_to_embed)

    for chunk, vector in zip(chunks, vectors):
        vector_index.upsert_vector(
            chunk_id=chunk["chunk_id"],
            document_id=chunk["document_id"],
            section_title=chunk["section_title"],
            status=document["status"],
            vector=vector,
        )

    return len(chunks)
