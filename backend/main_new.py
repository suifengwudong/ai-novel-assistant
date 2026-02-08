"""
API主应用
"""

from fastapi import FastAPI
from loguru import logger
from config.settings import settings
# 导入 v1 路由
from api.v1.api import api_router

# 创建应用
app = FastAPI(title="AI Novel Assistant", version="1.0.0")

# 挂载 v1 API 路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI Novel Assistant API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy", "environment": settings.app_env}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=False)