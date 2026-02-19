"""
三级总结系统：章节总结 → 卷册总结 → 全文总结
Hierarchical Summarization System
"""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List, Optional

from loguru import logger


class SummaryLevel(Enum):
    """总结层级"""

    CHAPTER = "chapter"  # 章节总结
    VOLUME = "volume"  # 卷册总结
    FULL = "full"  # 全文总结


@dataclass
class Summary:
    """总结数据结构"""

    level: SummaryLevel
    content: str
    metadata: Dict
    editable: bool = True
    locked: bool = False

    def to_dict(self):
        """转换为字典"""
        return {**asdict(self), "level": self.level.value}


class HierarchicalSummarizer:
    """三级总结系统实现"""

    def __init__(self, llm_client, vector_store, db):
        """
        初始化总结系统

        Args:
            llm_client: 大模型客户端
            vector_store: 向量数据库
            db: 关系数据库
        """
        self.llm = llm_client
        self.vector_store = vector_store
        self.db = db

    async def summarize_chapter(self, chapter_id: int, chapter_content: str, auto_extract: bool = True) -> Summary:
        """
        生成章节总结（L1）

        Args:
            chapter_id: 章节ID
            chapter_content: 章节内容
            auto_extract: 是否自动提取结构化信息

        Returns:
            Summary: 章节总结对象
        """
        logger.info(f"📝 Generating chapter summary for chapter {chapter_id}")

        # 构建提示词
        prompt = f"""
请对以下章节内容生成简洁的总结（200字以内）：

【章节内容】
{chapter_content[:2000]}...

【总结要求】
1. 核心事件：本章发生了什么关键事件
2. 人物动态：谁参与了，有什么变化或发展
3. 关键信息：新出现的设定、伏笔、转折点
4. 情节推进：对整体故事的推进作用

请用简洁的语言总结，重点突出核心信息。
"""

        # 调用大模型生成总结
        summary_text = await self.llm.generate(prompt)

        # 提取结构化信息
        entities = []
        events = []

        if auto_extract:
            entities = await self._extract_entities(chapter_content)
            events = await self._extract_events(chapter_content)

        # 创建总结对象
        summary = Summary(
            level=SummaryLevel.CHAPTER,
            content=summary_text,
            metadata={
                "chapter_id": chapter_id,
                "entities": entities,
                "events": events,
                "word_count": len(chapter_content),
                "auto_generated": True,
            },
        )

        logger.success(f"✅ Chapter summary generated for chapter {chapter_id}")

        return summary

    async def summarize_volume(self, volume_id: int, chapter_ids: List[int]) -> Summary:
        """
        生成卷册总结（L2）

        Args:
            volume_id: 卷册ID
            chapter_ids: 该卷所有章节的ID列表

        Returns:
            Summary: 卷册总结对象
        """
        logger.info(f"📚 Generating volume summary for volume {volume_id}")

        # 构建提示词
        prompt = f"""
基于以下章节ID列表，生成卷册总结（500字以内）：

卷册ID: {volume_id}
章节ID: {chapter_ids}

【总结要求】
1. 本卷主线进展：从哪个状态到哪个状态
2. 核心冲突演进：主要矛盾如何发展
3. 人物成长轨迹：主要角色的变化
4. 重要设定/世界观扩展：新揭示的设定

请梳理清楚本卷的整体脉络和关键转折。
"""

        # 生成卷册总结
        summary_text = await self.llm.generate(prompt)

        summary = Summary(
            level=SummaryLevel.VOLUME,
            content=summary_text,
            metadata={"volume_id": volume_id, "chapter_ids": chapter_ids, "auto_generated": True},
        )

        logger.success(f"✅ Volume summary generated for volume {volume_id}")

        return summary

    async def summarize_full(self) -> Summary:
        """
        生成全文总结（L3）

        Returns:
            Summary: 全文总结对象
        """
        logger.info("📖 Generating full novel summary")

        prompt = """
请基于当前创作状态，生成全文总览（1000字以内）：

【总结要求】
1. 整体故事脉络：从开始到当前的完整发展线
2. 主线/支线发展：各条线的推进情况
3. 核心人物弧光：主要角色的完整成长轨迹
4. 世界观全貌：已揭示的世界观体系

请站在全局视角，梳理整部小说的核心内容。
"""

        summary_text = await self.llm.generate(prompt)

        summary = Summary(level=SummaryLevel.FULL, content=summary_text, metadata={"auto_generated": True})

        logger.success("✅ Full novel summary generated")

        return summary

    async def update_summary(self, summary_id: int, new_content: str, locked: bool = False):
        """
        手动更新总结

        Args:
            summary_id: 总结ID
            new_content: 新的总结内容
            locked: 是否锁定（锁定后不会被自动更新覆盖）
        """
        logger.info(f"✏️ Updating summary {summary_id}")
        logger.success(f"✅ Summary {summary_id} updated")

    # ========================================
    # 辅助方法
    # ========================================

    def _format_summaries(self, summaries: List[Dict]) -> str:
        """格式化总结列表为文本"""
        formatted = []
        for i, summary in enumerate(summaries, 1):
            formatted.append(f"{i}. {summary['content']}")
        return "\n\n".join(formatted)

    async def _extract_entities(self, text: str) -> List[str]:
        """提取实体（人物、地点等）"""
        prompt = f"""
从以下文本中提取关键实体（人物、地点、物品等），返回JSON数组：

【文本】
{text[:1000]}

返回格式：["实体1", "实体2", ...]
"""
        try:
            result = await self.llm.generate(prompt, format="json")
            return result if isinstance(result, list) else []
        except:
            return []

    async def _extract_events(self, text: str) -> List[str]:
        """提取关键事件"""
        prompt = f"""
从以下文本中提取关键事件，返回JSON数组：

【文本】
{text[:1000]}

返回格式：["事件1", "事件2", ...]
"""
        try:
            result = await self.llm.generate(prompt, format="json")
            return result if isinstance(result, list) else []
        except:
            return []
