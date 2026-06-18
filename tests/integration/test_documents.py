import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.dependencies import get_app_settings
from app.main import app


@pytest.fixture
def client(tmp_path):
    settings = Settings(
        database_path=tmp_path / "rag.sqlite3",
        raw_data_dir=tmp_path / "raw",
    )
    app.dependency_overrides[get_app_settings] = lambda: settings
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def upload_file(client: TestClient, name: str, content: bytes):
    return client.post(
        "/documents/upload",
        files={"file": (name, content, "text/plain")},
    )


def test_upload_txt_file_creates_document_and_chunks(client: TestClient) -> None:
    response = upload_file(
        client,
        "sample.txt",
        b"First paragraph.\n\nSecond paragraph.",
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["duplicate"] is False
    assert payload["chunks_created"] == 2
    assert payload["document"]["file_name"] == "sample.txt"
    assert payload["document"]["source_type"] == "txt"

    chunks_response = client.get(
        f"/documents/{payload['document']['id']}/chunks"
    )
    chunks = chunks_response.json()["chunks"]
    assert len(chunks) == 2
    assert all(
        chunk["document_id"] == payload["document"]["id"] for chunk in chunks
    )


def test_upload_markdown_file_uses_heading_in_embedding_text(client: TestClient) -> None:
    response = upload_file(
        client,
        "sample.md",
        b"# Risk Factors\n\nSupply chain risk is discussed.",
    )

    assert response.status_code == 200
    document_id = response.json()["document"]["id"]
    chunks = client.get(f"/documents/{document_id}/chunks").json()["chunks"]

    assert chunks[0]["section_title"] == "Risk Factors"
    assert "Document: sample" in chunks[0]["embedding_text"]
    assert "Document Type: md" in chunks[0]["embedding_text"]
    assert "Section: Risk Factors" in chunks[0]["embedding_text"]
    assert not chunks[0]["text"].startswith("Document:")


def test_unsupported_file_rejected(client: TestClient) -> None:
    response = upload_file(client, "sample.pdf", b"%PDF-1.7")

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_duplicate_hash_detected(client: TestClient) -> None:
    first = upload_file(client, "first.txt", b"Same content.")
    second = upload_file(client, "second.txt", b"Same content.")

    assert first.status_code == 200
    assert second.status_code == 200
    assert second.json()["duplicate"] is True
    assert second.json()["document"]["id"] == first.json()["document"]["id"]

    documents = client.get("/documents").json()["documents"]
    assert len(documents) == 1
