"""
应用配置管理
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path


class Settings(BaseSettings):
    """应用配置类"""
    
    # ========================================
    # 大模型配置
    # ========================================
    LLM_PROVIDER: str = "openai"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4"
    LLM_BASE_URL: Optional[str] = None
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 4096
    
    # ========================================
    # 数据库配置
    # ========================================
    DATABASE_URL: str = "sqlite:///./data/novel_assistant.db"
    VECTOR_STORE_PATH: str = "./data/vector_store"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # ========================================
    # 应用配置
    # ========================================
    ENVIRONMENT: str = "development"
    API_PORT: int = 8000
    FRONTEND_PORT: int = 3000
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # ========================================
    # 功能配置
    # ========================================
    ENABLE_AUTO_BACKUP: bool = True
    BACKUP_INTERVAL_HOURS: int = 24
    EPHEMERAL_CACHE_TTL: int = 604800  # 7天
    VECTOR_SEARCH_TOP_K: int = 10
    
    # ========================================
    # 日志配置
    # ========================================
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # ========================================
    # 安全配置
    # ========================================
    JWT_SECRET_KEY: str = "your_secret_key_change_in_production"
    JWT_EXPIRE_DAYS: int = 30
    ENABLE_DATA_ENCRYPTION: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()


# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    dirs = [
        Path("./data"),
        Path("./data/vector_store"),
        Path("./data/redis"),
        Path("./logs"),
    ]
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)


ensure_directories()
