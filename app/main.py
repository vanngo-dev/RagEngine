from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_documents import router as documents_router
from api.routes_health import router as health_router
from api.routes_query import router as query_router
from api.routes_search import router as search_router
from app.config import get_settings
from app.logging_config import configure_logging


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="Robust Local RAG Engine",
    version=settings.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(search_router)
app.include_router(query_router)
