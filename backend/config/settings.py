from pydantic import BaseSettings

class Settings(BaseSettings):
    # LLM Configuration
    provider: str
    api_key: str
    model: str
    base_url: str
    temperature: float = 0.7
    max_tokens: int = 100

    # Database Configuration
    database_url: str
    vector_store_path: str
    redis_url: str

    # Application Configuration
    app_env: str = 'development'
    log_level: str = 'info'
    ports: list = [8000]
    cors_origins: list = ['*']

    # Feature Flags
    auto_summarize: bool = True
    auto_validate: bool = False
    cache_ttl: int = 3600  # Cache time in seconds

    # Security Settings
    secret_key: str
    token_expire: int = 3600  # Token expiration time in seconds

    # Performance Settings
    retrieval_top_k: int = 5
    max_chapter_length: int = 2000

# Global settings instance
settings = Settings()