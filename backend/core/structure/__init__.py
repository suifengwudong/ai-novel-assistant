"""
结构化创作引擎 (Gardener Mode)
Phase 4: 实时监控与反馈系统

这个模块提供了小说创作的结构化支持，包括：
- 大纲守卫：监控写作偏离度
- 伏笔追踪器：管理未闭合的剧情线
- 节奏分析器：基于字数和情绪曲线分析
"""

from .models import (
    PlotNode, NovelProject, PlotLoop,
    NodeType, NodeStatus, PacingTemplate
)
from .guardian import OutlineGuardian
from .loop_tracker import LoopTracker
from .pacer import PacingAnalyzer

__all__ = [
    # 数据模型
    "PlotNode", "NovelProject", "PlotLoop",
    "NodeType", "NodeStatus", "PacingTemplate",

    # 核心组件
    "OutlineGuardian",
    "LoopTracker",
    "PacingAnalyzer"
]