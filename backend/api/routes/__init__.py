"""
API路由模块
"""
from .agent import router as agent_router
from .auth import router as auth_router
from .collaboration import router as collab_router
from .export import router as export_router
from .projects import router as project_router
from .style import router as style_router

__all__ = ["style_router", "agent_router", "project_router", "auth_router", "export_router", "collab_router"]
