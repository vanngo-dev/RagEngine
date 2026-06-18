from fastapi.testclient import TestClient

from app.main import app


def test_app_imports_successfully() -> None:
    assert app.title == "Robust Local RAG Engine"


def test_health_endpoint_returns_expected_response() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "rag-engine",
        "version": "0.1.0",
    }
