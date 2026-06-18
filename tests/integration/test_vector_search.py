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


def test_embed_endpoint_and_vector_search_retrieve_chunks(client: TestClient) -> None:
    upload = client.post(
        "/documents/upload",
        files={
            "file": (
                "risk.md",
                b"# Risk Factors\n\nSupply chain delays are a risk factor.",
                "text/markdown",
            )
        },
    )
    document_id = upload.json()["document"]["id"]

    embed = client.post(f"/documents/{document_id}/embed")
    search = client.post(
        "/search/vector",
        json={"query": "supply chain risk factors", "top_k": 5},
    )

    assert embed.status_code == 200
    assert embed.json()["embedded_chunks"] == 1
    assert search.status_code == 200
    results = search.json()["results"]
    assert results[0]["document_id"] == document_id
    assert results[0]["text"] == "Supply chain delays are a risk factor."
    assert results[0]["metadata"]["section_title"] == "Risk Factors"
