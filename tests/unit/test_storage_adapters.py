import pytest

from app.config import Settings
from rag_engine.interfaces import (
    CitationVerifier,
    ChunkStore,
    DocumentStore,
    EmbeddingProvider,
    JobStore,
    KeywordIndex,
    LLMProvider,
    RerankerProvider,
    VectorIndex,
)
from rag_engine.storage.factory import (
    get_document_store_for_profile,
    get_job_store_for_profile,
    get_keyword_index_for_profile,
    get_vector_index_for_profile,
)


def test_storage_profile_loads_default_local_lite() -> None:
    assert Settings().storage_profile == "local_lite"


def test_local_lite_still_works_through_interfaces(tmp_path) -> None:
    store = get_document_store_for_profile("local_lite", tmp_path / "rag.sqlite3")
    document = store.create_document(
        document_id="doc_interface",
        title="Interface",
        file_name="interface.md",
        file_path="interface.md",
        source_type="md",
        content_hash="interface_hash",
        status="active",
    )

    assert document["id"] == "doc_interface"
    assert store.get_document("doc_interface")["title"] == "Interface"


def test_placeholder_adapters_raise_clear_error(tmp_path) -> None:
    with pytest.raises(NotImplementedError, match="postgres adapter is a placeholder"):
        get_document_store_for_profile("postgres", tmp_path / "rag.sqlite3")

    with pytest.raises(NotImplementedError, match="qdrant adapter is a placeholder"):
        get_vector_index_for_profile("qdrant", tmp_path / "rag.sqlite3")

    with pytest.raises(NotImplementedError, match="opensearch adapter is a placeholder"):
        get_keyword_index_for_profile("opensearch", tmp_path / "rag.sqlite3")

    with pytest.raises(NotImplementedError, match="redis_jobs adapter is a placeholder"):
        get_job_store_for_profile("redis_jobs")


def test_required_interface_names_exist() -> None:
    assert DocumentStore
    assert ChunkStore
    assert VectorIndex
    assert KeywordIndex
    assert JobStore
    assert EmbeddingProvider
    assert LLMProvider
    assert RerankerProvider
    assert CitationVerifier
