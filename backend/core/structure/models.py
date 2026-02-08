"""
小说项目核心数据结构
用于Phase 4: 结构化创作引擎 (Gardener Mode)
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import datetime
from enum import Enum

class NodeType(Enum):
    """节点类型枚举"""
    VOLUME = "volume"    # 卷
    CHAPTER = "chapter"  # 章
    SCENE = "scene"      # 场景

class NodeStatus(Enum):
    """节点状态枚举"""
    DRAFT = "draft"      # 草稿
    WRITING = "writing"  # 写作中
    FINISHED = "finished"  # 已完成

class PacingTemplate(Enum):
    """节奏模板枚举"""
    HERO_JOURNEY = "hero_journey"  # 英雄之旅
    THREE_ACT = "three_act"        # 三幕结构
    SAVE_THE_CAT = "save_the_cat"  # 救猫咪
    CUSTOM = "custom"              # 自定义

@dataclass
class PlotNode:
    """大纲节点 (可以是卷、章、或具体场景)"""
    id: str
    title: str
    description: str  # 预设的大纲内容
    type: NodeType

    # 状态追踪
    status: NodeStatus = NodeStatus.DRAFT
    actual_content_summary: str = ""  # AI生成的正文实际总结
    deviation_score: float = 0.0      # 偏离度 (0-1)

    # 关联信息
    characters: List[str] = field(default_factory=list)
    open_loops: List[str] = field(default_factory=list)  # 本节埋下的伏笔
    closed_loops: List[str] = field(default_factory=list)  # 本节回收的伏笔

    # 元数据
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    word_count: int = 0  # 实际字数
    estimated_word_count: int = 0  # 预估字数

    # 树状结构关系
    parent_id: Optional[str] = None
    children_ids: List[str] = field(default_factory=list)

    def __post_init__(self):
        """数据验证"""
        if not self.id:
            raise ValueError("节点ID不能为空")
        if not self.title:
            raise ValueError("节点标题不能为空")
        if self.deviation_score < 0 or self.deviation_score > 1:
            raise ValueError("偏离度必须在0-1之间")

@dataclass
class PlotLoop:
    """伏笔/悬念对象"""
    id: str
    description: str  # 伏笔描述
    created_in_node: str  # 在哪个节点中创建
    resolved_in_node: Optional[str] = None  # 在哪个节点中解决
    status: Literal["open", "resolved", "abandoned"] = "open"
    importance: Literal["minor", "major", "critical"] = "minor"

    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None

@dataclass
class PacingCheckpoint:
    """节奏检查点"""
    position: float  # 故事进度 (0-1)
    expected_tension: int  # 预期紧张度 (1-10)
    description: str  # 检查点描述
    template: PacingTemplate

@dataclass
class NovelProject:
    """小说项目"""
    id: str
    title: str
    outline_tree: List[PlotNode]  # 树状结构

    # 全局节奏配置
    target_word_count: int = 200000
    pacing_template: PacingTemplate = PacingTemplate.HERO_JOURNEY

    # 项目状态
    current_node_id: Optional[str] = None  # 当前正在写作的节点
    total_word_count: int = 0
    completion_percentage: float = 0.0

    # 伏笔追踪
    open_loops: List[PlotLoop] = field(default_factory=list)
    resolved_loops: List[PlotLoop] = field(default_factory=list)

    # 元数据
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """数据验证"""
        if not self.id:
            raise ValueError("项目ID不能为空")
        if not self.title:
            raise ValueError("项目标题不能为空")
        if self.target_word_count <= 0:
            raise ValueError("目标字数必须大于0")
        if self.completion_percentage < 0 or self.completion_percentage > 1:
            raise ValueError("完成百分比必须在0-1之间")

    def get_node_by_id(self, node_id: str) -> Optional[PlotNode]:
        """根据ID获取节点"""
        for node in self.outline_tree:
            if node.id == node_id:
                return node
        return None

    def get_open_loops_count(self) -> int:
        """获取未解决的伏笔数量"""
        return len([loop for loop in self.open_loops if loop.status == "open"])

    def update_completion_percentage(self):
        """更新完成百分比"""
        if not self.outline_tree:
            self.completion_percentage = 0.0
            return

        finished_nodes = sum(1 for node in self.outline_tree if node.status == NodeStatus.FINISHED)
        self.completion_percentage = finished_nodes / len(self.outline_tree)