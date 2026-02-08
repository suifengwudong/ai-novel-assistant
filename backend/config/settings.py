from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    provider: str = "ollama"
    api_key: str = "ollama"
    model: str = "ollama/qwen2.5:14b"
    base_url: str = "http://localhost:11434"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    database_url: str = "sqlite:///./data/novel_assistant.db"
    vector_store_path: str = "./data/vector_store"
    redis_url: str = "redis://localhost:6379/0"
    
    app_env: str = "development"
    api_port: int = 8000
    frontend_port: int = 3000
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    enable_auto_backup: bool = True
    backup_interval_hours: int = 24
    ephemeral_cache_ttl: int = 604800
    vector_search_top_k: int = 10
    
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    secret_key: str = "your_secret_key_change_in_production"
    jwt_expire_days: int = 30
    enable_data_encryption: bool = True

# Global settings instance
settings = Settings()