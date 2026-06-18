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


def test_debug_endpoint_includes_required_fields_with_mocked_llm(client: TestClient) -> None:
    upload = client.post(
        "/documents/upload",
        files={
            "file": (
                "overview.md",
                b"# Overview\n\nThe document is about debug traces.",
                "text/markdown",
            )
        },
    )
    document_id = upload.json()["document"]["id"]
    client.post(f"/documents/{document_id}/embed")

    response = client.post(
        "/query/debug",
        json={"question": "What is this document about?"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["question"] == "What is this document about?"
    assert payload["vector_results"]
    assert "SOURCE S1" in payload["selected_context"]
    assert "Use only the provided sources." in payload["prompt_preview"]
    assert payload["answer"] == "The document is about debug traces. [S1]"
    assert payload["citations"][0]["source_id"] == "S1"
    assert len(payload["prompt_preview"]) <= 1003
    assert payload["rerank_results"]
    assert payload["selected_evidence"]["primary_evidence"]
    assert payload["structured_claims"]["claims"]
    assert payload["verification"]["passed"] is True
    assert payload["verification_attempts"] == 1
    assert payload["confidence_signals"]["positive"]
