from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    environment: str = "development"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    request_timeout_seconds: int = 60
    enable_local_explanation: bool = False
    local_model_name: str = "MBZUAI/LaMini-Flan-T5-783M"
    max_input_chars: int = 12000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
