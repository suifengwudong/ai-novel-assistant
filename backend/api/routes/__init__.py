"""
API路由模块
"""
from .style import router as style_router
from .agent import router as agent_router

__all__ = ["style_router", "agent_router"]

