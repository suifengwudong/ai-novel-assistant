"""
读者反馈模拟器
模拟不同类型读者的评论和反馈
"""
from typing import List, Dict
from loguru import logger
from enum import Enum

class ReaderType(Enum):
    CASUAL = "casual"       # 小白读者：看重爽点、节奏，不带脑子
    CRITICAL = "critical"   # 老白读者：看重逻辑、文笔，毒点低
    LORE = "lore"          # 考据党：看重设定严谨性，喜欢挑刺
    EMOTIONAL = "emotional" # 情感党：看重CP、人物情感

class FeedbackSimulator:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def simulate_feedback(self, content: str, reader_types: List[ReaderType]) -> Dict[str, List[str]]:
        """模拟多类型读者的反馈"""
        logger.info("正在生成模拟读者反馈...")

        feedbacks = {}

        for reader in reader_types:
            persona = self._get_reader_persona(reader)
            prompt = f"""
请扮演一位{persona['name']}。
{persona['description']}

阅读以下小说片段，发表3条简短犀利的评论（书评/章评）。
如果是好评请点赞，如果是毒点请毫不留情地吐槽。

【小说片段】
{content[:2000]}

返回格式（每行一条评论）：
"""
            try:
                comments_text = await self.llm.generate(prompt)
                comments = [c.strip() for c in comments_text.split('\n') if c.strip()]
                feedbacks[reader.value] = comments
                logger.info(f"生成 {reader.value} 类型读者反馈: {len(comments)} 条")
            except Exception as e:
                logger.error(f"Feedback simulation failed for {reader.value}: {e}")
                feedbacks[reader.value] = []

        return feedbacks

    def _get_reader_persona(self, reader_type: ReaderType) -> Dict:
        personas = {
            ReaderType.CASUAL: {
                "name": "爽文爱好者",
                "description": "你喜欢快节奏、装逼打脸、无脑爽的剧情。讨厌压抑、虐主、谜语人和慢热。关注点是主角爽不爽。"
            },
            ReaderType.CRITICAL: {
                "name": "资深老书虫",
                "description": "你阅读量极大，口味刁钻。看重逻辑自洽、人物智商在线、文笔老练。极其讨厌降智光环、套路化剧情和OOC。"
            },
            ReaderType.LORE: {
                "name": "设定考据党",
                "description": "你拿着放大镜看书，关注世界观设定是否严谨，数据是否合理。一旦发现设定冲突或常识错误就会疯狂吐槽。"
            },
            ReaderType.EMOTIONAL: {
                "name": "情感共鸣者",
                "description": "你非常感性，关注人物命运和情感纠葛。容易被感动，也容易因为发刀片而愤怒。特别关注CP互动。"
            }
        }
        return personas[reader_type]