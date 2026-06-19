from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with local-development defaults."""

    service_name: str = Field(default="rag-engine", alias="SERVICE_NAME")
    version: str = Field(default="0.1.0", alias="SERVICE_VERSION")
    environment: str = Field(default="local", alias="ENVIRONMENT")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    storage_profile: str = Field(default="local_lite", alias="STORAGE_PROFILE")
    postgres_dsn: str = Field(
        default="postgresql://rag:rag@localhost:5432/rag_engine",
        alias="POSTGRES_DSN",
    )
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    qdrant_collection: str = Field(
        default="rag_chunks",
        alias="QDRANT_COLLECTION",
    )
    opensearch_url: str = Field(
        default="http://localhost:9200",
        alias="OPENSEARCH_URL",
    )
    opensearch_index: str = Field(
        default="rag_chunks",
        alias="OPENSEARCH_INDEX",
    )
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")
    database_path: Path = Field(
        default=Path("data/processed/rag_engine.sqlite3"),
        alias="DATABASE_PATH",
    )
    raw_data_dir: Path = Field(default=Path("data/raw"), alias="RAW_DATA_DIR")
    chunk_max_tokens: int = Field(default=180, alias="CHUNK_MAX_TOKENS")
    embedding_provider: str = Field(default="fake", alias="EMBEDDING_PROVIDER")
    llm_provider: str = Field(default="mock", alias="LLM_PROVIDER")
    reranker_provider: str = Field(default="mock", alias="RERANKER_PROVIDER")
    cors_allowed_origins: list[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        alias="CORS_ALLOWED_ORIGINS",
    )
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
    )
    ollama_model: str = Field(default="llama3.1", alias="OLLAMA_MODEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
