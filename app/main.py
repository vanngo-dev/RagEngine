from fastapi import FastAPI

from api.routes_documents import router as documents_router
from api.routes_health import router as health_router
from app.config import get_settings
from app.logging_config import configure_logging


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="Robust Local RAG Engine",
    version=settings.version,
)

app.include_router(health_router)
app.include_router(documents_router)
