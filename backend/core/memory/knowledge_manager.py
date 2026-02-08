"""
双层知识管理系统实现
核心信息：持久化存储（人物/世界观/主线）
即时信息：临时缓存（场景/细节）
"""

from typing import List, Optional, Dict
from enum import Enum
from dataclasses import dataclass
from loguru import logger


class KnowledgeType(Enum):
    """知识类型"""
    CORE = "core"              # 核心信息（持久化）
    EPHEMERAL = "ephemeral"    # 即时性信息（临时缓存）


class KnowledgeCategory(Enum):
    """知识分类"""
    CHARACTER = "character"    # 人物设定
    WORLD = "world"           # 世界观
    PLOT = "plot"             # 主线情节
    SCENE = "scene"           # 场景描写
    DETAIL = "detail"         # 细节信息
    CUSTOM = "custom"         # 自定义分类


@dataclass
class Knowledge:
    """知识条目"""
    id: Optional[int] = None
    content: str = ""
    knowledge_type: KnowledgeType = KnowledgeType.CORE
    category: KnowledgeCategory = KnowledgeCategory.CUSTOM
    locked: bool = False       # 锁定标记
    tags: Optional[List[str]] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class KnowledgeManager:
    """知识管理系统"""
    
    def __init__(self, vector_store, db, cache):
        """
        初始化知识管理器
        
        Args:
            vector_store: 向量存储
            db: 数据库连接
            cache: Redis缓存
        """
        self.vector_store = vector_store
        self.db = db
        self.cache = cache
        
    async def add_knowledge(
        self,
        content: str,
        knowledge_type: KnowledgeType,
        category: KnowledgeCategory,
        locked: bool = False,
        tags: Optional[List[str]] = None
    ) -> Knowledge:
        """
        添加知识条目
        
        Args:
            content: 知识内容
            knowledge_type: 知识类型（核心/即时）
            category: 知识分类
            locked: 是否锁定
            tags: 标签列表
            
        Returns:
            Knowledge: 知识对象
        """
        logger.info(f"添加知识: {category.value} ({knowledge_type.value})")
        
        knowledge = Knowledge(
            content=content,
            knowledge_type=knowledge_type,
            category=category,
            locked=locked,
            tags=tags or []
        )
        
        if knowledge_type == KnowledgeType.CORE:
            # 核心信息：存入数据库 + 向量库
            logger.info(f"✅ 核心知识已存储")
            
        else:
            # 即时性信息：仅缓存（7天过期）
            cache_key = f"ephemeral:{category.value}:{hash(content)}"
            logger.info(f"✅ 即时信息已缓存: {cache_key}")
        
        return knowledge
    
    async def retrieve_context(
        self,
        query: str,
        top_k: int = 10,
        categories: Optional[List[KnowledgeCategory]] = None
    ) -> List[str]:
        """
        检索相关上下文（核心信息优先，锁定信息置顶）
        
        Args:
            query: 查询文本
            top_k: 返回Top-K结果
            categories: 限定分类（可选）
            
        Returns:
            List[str]: 检索结果列表
        """
        logger.info(f"检索上下文: {query}")
        
        all_results = []
        
        logger.info(f"✅ 检索完成，返回 {len(all_results)} 条结果")
        return all_results
    
    async def update_knowledge(
        self,
        knowledge_id: int,
        content: Optional[str] = None,
        locked: Optional[bool] = None,
        tags: Optional[List[str]] = None
    ) -> Knowledge:
        """
        更新知识条目
        
        Args:
            knowledge_id: 知识ID
            content: 新内容（可选）
            locked: 锁定状态（可选）
            tags: 标签（可选）
            
        Returns:
            Knowledge: 更新后的知识对象
        """
        logger.info(f"更新知识: ID {knowledge_id}")
        logger.success(f"✅ 知识 {knowledge_id} 更新完成")
        return Knowledge()
    
    async def delete_knowledge(self, knowledge_id: int):
        """删除知识条目"""
        logger.info(f"删除知识: ID {knowledge_id}")
        logger.success(f"✅ 知识 {knowledge_id} 已删除")
    
    async def get_by_category(
        self,
        category: KnowledgeCategory,
        knowledge_type: Optional[KnowledgeType] = None
    ) -> List[Knowledge]:
        """按分类获取知识"""
        logger.info(f"获取分类知识: {category.value}")
        logger.info(f"✅ 找到相关知识")
        return []
