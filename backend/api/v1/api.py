from fastapi import APIRouter
from api.v1.endpoints import knowledge, guardian, generation

api_router = APIRouter()

# 挂载各个模块的路由
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge"])
api_router.include_router(guardian.router, prefix="/guardian", tags=["Guardian"])
api_router.include_router(generation.router, prefix="/generation", tags=["Generation"])