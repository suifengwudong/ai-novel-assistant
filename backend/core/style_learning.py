"""
风格学习系统
分析样章并提取风格特征，用于指导生成
"""
from typing import Dict, List, Optional
from loguru import logger
from dataclasses import dataclass, asdict

@dataclass
class StyleProfile:
    """风格画像"""
    id: str
    name: str
    lexical_features: List[str]  # 用词特征
    sentence_patterns: List[str] # 句式模式
    rhetorical_devices: List[str] # 修辞手法
    tone: str # 整体基调

    def to_dict(self):
        return asdict(self)

class StyleLearner:
    def __init__(self, llm_client, db):
        self.llm = llm_client
        self.db = db # 假设是一个可以存取 JSON/Blob 的数据库接口

    async def analyze_style(self, sample_text: str, style_name: str) -> StyleProfile:
        """从样章中提取风格特征"""
        logger.info(f"正在分析风格: {style_name}")

        prompt = f"""
请作为一名文学评论家，深入分析以下文本的写作风格：

【样章文本】
{sample_text[:3000]}

请从以下维度进行提取：
1. 用词特征（如：古风辞藻、赛博朋克黑话、平实口语等）
2. 句式习惯（如：长短句结合、多用倒装、流水账等）
3. 修辞手法（如：善用比喻、心理描写细腻、白描等）
4. 整体基调（如：压抑、轻松、热血、悬疑等）

返回 JSON 格式：
{{
    "lexical_features": ["特征1", "特征2"],
    "sentence_patterns": ["习惯1", "习惯2"],
    "rhetorical_devices": ["手法1", "手法2"],
    "tone": "基调描述"
}}
"""
        try:
            result = await self.llm.generate(prompt) # Remove format="json" for broad compatibility

            # 简单的 JSON 提取
            import json
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                json_str = result.split("```")[1].split("```")[0].strip()
            else:
                json_str = result

            data = json.loads(json_str)

            profile = StyleProfile(
                id=f"style_{hash(style_name)}",
                name=style_name,
                lexical_features=data.get("lexical_features", []),
                sentence_patterns=data.get("sentence_patterns", []),
                rhetorical_devices=data.get("rhetorical_devices", []),
                tone=data.get("tone", "default")
            )

            # 保存到数据库 (Mock)
            # await self.db.save_style(profile.to_dict())
            logger.success(f"风格分析完成: {style_name}")
            return profile

        except Exception as e:
            logger.error(f"风格分析失败: {e}")
            # 返回默认画像
            return StyleProfile("default", "Default", [], [], [], "Neutral")

    def get_style_prompt(self, profile: StyleProfile) -> str:
        """生成用于指导写作的 Prompt 片段"""
        return f"""
【写作风格要求】
请严格模仿以下风格进行创作：
- 用词偏好：{', '.join(profile.lexical_features)}
- 句式结构：{', '.join(profile.sentence_patterns)}
- 修辞手法：{', '.join(profile.rhetorical_devices)}
- 整体基调：{profile.tone}
"""