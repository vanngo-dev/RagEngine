from app.config import Settings, get_settings


def test_config_loads_with_defaults() -> None:
    settings = Settings()

    assert settings.service_name == "rag-engine"
    assert settings.version == "0.1.0"
    assert settings.environment == "local"


def test_get_settings_returns_settings() -> None:
    assert isinstance(get_settings(), Settings)
