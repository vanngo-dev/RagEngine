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


def upload(client: TestClient, name: str, text: str, entity: str) -> str:
    response = client.post(
        "/documents/upload",
        data={
            "entity": entity,
            "document_type": "policy",
            "document_date": "2026-01-01",
        },
        files={"file": (name, text.encode("utf-8"), "text/markdown")},
    )
    document_id = response.json()["document"]["id"]
    client.post(f"/documents/{document_id}/embed")
    return document_id


def test_superseded_document_hidden_by_default_and_included_when_requested(
    client: TestClient,
) -> None:
    old_id = upload(
        client,
        "old.md",
        "# Risk\n\nLegacy risk factors include old supplier delays.",
        "Acme",
    )
    new_id = upload(
        client,
        "new.md",
        "# Risk\n\nCurrent risk factors include new supplier delays.",
        "Acme",
    )

    supersede = client.post(
        f"/documents/{old_id}/supersede",
        json={"new_document_id": new_id},
    )
    default_search = client.post(
        "/search/vector",
        json={"query": "legacy old supplier delays", "top_k": 10},
    )
    historical_search = client.post(
        "/search/vector",
        json={
            "query": "legacy old supplier delays",
            "top_k": 10,
            "include_superseded": True,
        },
    )

    assert supersede.status_code == 200
    assert supersede.json()["superseded_document"]["status"] == "superseded"
    assert old_id not in {
        result["document_id"] for result in default_search.json()["results"]
    }
    assert old_id in {
        result["document_id"] for result in historical_search.json()["results"]
    }


def test_metadata_filters_apply_to_vector_keyword_and_hybrid_search(
    client: TestClient,
) -> None:
    acme_id = upload(
        client,
        "acme.md",
        "# Risk\n\nRisk factors include supplier delays for Acme.",
        "Acme",
    )
    upload(
        client,
        "beta.md",
        "# Risk\n\nRisk factors include supplier delays for Beta.",
        "Beta",
    )

    request = {
        "query": "risk factors supplier",
        "top_k": 10,
        "entity": "Acme",
        "document_type": "policy",
    }

    for endpoint in ("/search/vector", "/search/keyword", "/search/hybrid"):
        response = client.post(endpoint, json=request)
        document_ids = {result["document_id"] for result in response.json()["results"]}
        assert document_ids == {acme_id}
