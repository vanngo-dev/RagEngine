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
    database_path: Path = Field(
        default=Path("data/processed/rag_engine.sqlite3"),
        alias="DATABASE_PATH",
    )
    raw_data_dir: Path = Field(default=Path("data/raw"), alias="RAW_DATA_DIR")
    chunk_max_tokens: int = Field(default=180, alias="CHUNK_MAX_TOKENS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
