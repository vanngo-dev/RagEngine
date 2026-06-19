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


def test_dev_cors_allows_vite_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
