"""
API主应用
"""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from api.routes import agent_router, style_router
from config.settings import settings


# 应用生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动和关闭时的处理"""
    # 启动时初始化
    try:
        logger.info("🚀 Starting AI Novel Assistant...")
        logger.info(f"Environment: {settings.ENVIRONMENT}")
        logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

    yield

    # 关闭时清理
    try:
        logger.info("👋 Shutting down AI Novel Assistant...")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# 创建FastAPI应用
app = FastAPI(
    title="AI Novel Assistant API",
    description="基于智能体的小说创作助手 API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载 API 路由
app.include_router(style_router, prefix="/api/v1")
app.include_router(agent_router, prefix="/api/v1")


# ========================================
# 健康检查
# ========================================


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "version": "0.1.0", "environment": settings.ENVIRONMENT}


@app.get("/")
async def root():
    """根路径"""
    return {"message": "🎨 AI Novel Assistant API", "docs": "/docs", "health": "/health"}


# ========================================
# 全局异常处理
# ========================================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP异常处理"""
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail, "status_code": exc.status_code})


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """通用异常处理"""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.ENVIRONMENT == "development" else None,
        },
    )


# ========================================
# API 路由挂载
# ========================================

app.include_router(style_router, prefix="/api/v1")
app.include_router(agent_router, prefix="/api/v1")


# ========================================
# 应用入口
# ========================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=settings.ENVIRONMENT == "development",
        log_level=settings.LOG_LEVEL.lower(),
    )
