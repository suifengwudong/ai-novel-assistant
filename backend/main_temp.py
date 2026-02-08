"""
API主应用
"""

from fastapi import FastAPI
from loguru import logger

# 创建应用
app = FastAPI(title="AI Novel Assistant", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "AI Novel Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)