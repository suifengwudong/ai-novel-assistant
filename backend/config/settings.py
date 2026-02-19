from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env", extra="ignore")

    # LLM configuration (env vars: LLM_PROVIDER, LLM_API_KEY, LLM_MODEL, LLM_BASE_URL)
    LLM_PROVIDER: str = Field(default="ollama", alias="LLM_PROVIDER")
    LLM_API_KEY: str = Field(default="ollama", alias="LLM_API_KEY")
    LLM_MODEL: str = Field(default="ollama/qwen2.5:14b", alias="LLM_MODEL")
    LLM_BASE_URL: str = Field(default="http://localhost:11434", alias="LLM_BASE_URL")
    LLM_TEMPERATURE: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    LLM_MAX_TOKENS: int = Field(default=4096, alias="LLM_MAX_TOKENS")

    # Database
    DATABASE_URL: str = Field(default="sqlite:///./data/novel_assistant.db", alias="DATABASE_URL")
    VECTOR_STORE_PATH: str = Field(default="./data/vector_store", alias="VECTOR_STORE_PATH")
    REDIS_URL: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # Application
    ENVIRONMENT: str = Field(default="development", alias="APP_ENV")
    API_PORT: int = Field(default=8000, alias="BACKEND_PORT")
    FRONTEND_PORT: int = Field(default=3000, alias="FRONTEND_PORT")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000"],
        alias="CORS_ORIGINS"
    )

    # Feature flags
    ENABLE_AUTO_BACKUP: bool = Field(default=True, alias="ENABLE_AUTO_BACKUP")
    BACKUP_INTERVAL_HOURS: int = Field(default=24, alias="BACKUP_INTERVAL_HOURS")
    EPHEMERAL_CACHE_TTL: int = Field(default=604800, alias="EPHEMERAL_CACHE_TTL")
    VECTOR_SEARCH_TOP_K: int = Field(default=10, alias="VECTOR_SEARCH_TOP_K")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", alias="LOG_LEVEL")
    LOG_FILE: str = Field(default="./logs/app.log", alias="LOG_FILE")

    # Security
    SECRET_KEY: str = Field(default="your_secret_key_change_in_production", alias="SECRET_KEY")
    JWT_EXPIRE_DAYS: int = Field(default=30, alias="JWT_EXPIRE_DAYS")

# Global settings instance
settings = Settings()