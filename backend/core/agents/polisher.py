"""
润色优化 Agent
对草稿进行精修，提升文学性
"""
from typing import Dict, Any
from loguru import logger

class PolishingAgent:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def polish(self, content: str, focus: str = "general") -> str:
        """
        对内容进行润色

        Args:
            content: 原始内容
            focus: 润色侧重点 (general/descriptive/emotional/action)
        """
        logger.info(f"开始润色内容，侧重点: {focus}")

        focus_prompts = {
            "general": "提升整体文笔流畅度和文学性，修正语病。",
            "descriptive": "加强环境和细节描写，增强画面感，多用视听嗅味触五感描写。",
            "emotional": "深入挖掘人物内心活动，增强情感渲染力和感染力。",
            "action": "精简冗余文字，加快叙事节奏，使动作描写更凌厉更有张力。"
        }

        instruction = focus_prompts.get(focus, focus_prompts["general"])

        prompt = f"""
你是一名资深小说编辑。请对以下段落进行润色。

【润色要求】
{instruction}
注意：只修改文笔，严禁改动原有情节走向和人物关系！

【原文】
{content}

【润色后】
"""
        try:
            result = await self.llm.generate(prompt)
            logger.success(f"润色完成，原始长度: {len(content)} -> 润色后长度: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"Polishing failed: {e}")
            return content # 失败则返回原文