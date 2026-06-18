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


def test_fts_keyword_search_and_exact_phrase(client: TestClient) -> None:
    client.post(
        "/documents/upload",
        files={
            "file": (
                "risk.md",
                b"# Risk\n\nRisk factors include supplier delays.",
                "text/markdown",
            )
        },
    )

    keyword = client.post(
        "/search/keyword",
        json={"query": "risk factors", "top_k": 10},
    )
    phrase = client.post(
        "/search/keyword",
        json={"query": "\"risk factors\"", "top_k": 10},
    )

    assert keyword.status_code == 200
    assert keyword.json()["results"][0]["text"] == "Risk factors include supplier delays."
    assert phrase.json()["results"][0]["text"] == "Risk factors include supplier delays."


def test_hybrid_search_returns_candidates_from_both_systems(client: TestClient) -> None:
    upload = client.post(
        "/documents/upload",
        files={
            "file": (
                "risk.md",
                b"# Risk Factors\n\nSupply chain risk factors are tracked.",
                "text/markdown",
            )
        },
    )
    document_id = upload.json()["document"]["id"]
    client.post(f"/documents/{document_id}/embed")

    response = client.post(
        "/search/hybrid",
        json={"query": "supply chain risk factors", "top_k": 10},
    )

    result = response.json()["results"][0]
    assert response.status_code == 200
    assert result["document_id"] == document_id
    assert result["ranking_signals"]["sources"] == ["keyword", "vector"]
    assert "keyword" in result["ranking_signals"]["ranks"]
    assert "vector" in result["ranking_signals"]["ranks"]
