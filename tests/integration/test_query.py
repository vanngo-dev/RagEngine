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


def test_query_response_includes_answer_and_citations(client: TestClient) -> None:
    upload = client.post(
        "/documents/upload",
        files={
            "file": (
                "overview.md",
                b"# Overview\n\nThe document is about supply chain risk.",
                "text/markdown",
            )
        },
    )
    document_id = upload.json()["document"]["id"]
    client.post(f"/documents/{document_id}/embed")

    response = client.post(
        "/query",
        json={"question": "What is this document about?"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["answer"] == "The document is about supply chain risk. [S1]"
    assert payload["citations"][0]["source_id"] == "S1"
    assert payload["citations"][0]["document_id"] == document_id
