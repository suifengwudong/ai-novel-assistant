"""
伏笔/悬念追踪器 (Open Loops Tracker)
防止作者"挖坑不填"
"""
import json
import re
from typing import List, Dict, Optional
from loguru import logger
from backend.core.structure.models import PlotLoop, NovelProject, PlotNode

class LoopTracker:
    """
    伏笔追踪器 - 管理未闭合的剧情线

    核心功能：
    1. 自动识别新伏笔
    2. 追踪伏笔状态
    3. 检测伏笔回收
    4. 生成伏笔报告
    """

    def __init__(self, db_client, llm_client):
        self.db = db_client
        self.llm = llm_client

    async def scan_for_new_loops(self, content: str, node_id: str) -> List[PlotLoop]:
        """
        扫描正文，发现新埋下的伏笔

        Args:
            content: 待分析的文本内容
            node_id: 当前节点ID

        Returns:
            新发现的伏笔列表
        """
        logger.info(f"正在扫描新伏笔... 节点: {node_id}")

        if not content.strip():
            return []

        # 预处理文本，移除过短的内容
        if len(content) < 100:
            logger.info("内容过短，跳过伏笔扫描")
            return []

        prompt = f"""
你是一位专业的文学编辑，专门负责识别小说中的伏笔和悬念设置。

请分析以下文本，找出所有新出现的"未解之谜"或"伏笔"。伏笔定义：作者故意留下的线索，暗示未来会发生什么，或者暂时不解释的异常现象。

【分析要点】
1. **明确的伏笔**: "主角捡到的戒指发光了，但不知道为什么"
2. **人物之谜**: "反派临死前说'组织不会放过你'"
3. **世界观线索**: "地图上标记了一个不存在的城市"
4. **能力暗示**: "主角在危急时刻展现了超出常人的直觉"
5. **物品之谜**: "古董店老板送给主角一本奇怪的书"
6. **关系线索**: "陌生人说'你和你父亲很像'"

【排除项目】
- 日常对话和描述
- 已解释清楚的内容
- 纯属比喻的表达
- 过于明显的剧情发展

文本内容：
{content[:3000]}...

请返回JSON格式的伏笔列表：
[
    {{
        "description": "具体的伏笔描述",
        "importance": "minor/major/critical",
        "category": "character/world/item/ability/relationship/other",
        "confidence": 0.0-1.0
    }}
]

只返回JSON数组，不要其他说明。
"""

        try:
            result_text = await self.llm.generate(prompt, temperature=0.2)
            result_text = self._clean_json_response(result_text)

            loops_data = json.loads(result_text)

            if not isinstance(loops_data, list):
                logger.warning("LLM返回的不是数组格式")
                return []

            new_loops = []
            for i, loop_data in enumerate(loops_data):
                try:
                    # 验证数据结构
                    if not isinstance(loop_data, dict) or "description" not in loop_data:
                        continue

                    loop = PlotLoop(
                        id=f"{node_id}_loop_{i+1}",
                        description=loop_data["description"],
                        created_in_node=node_id,
                        status="open",
                        importance=loop_data.get("importance", "minor")
                    )

                    # 验证重要性等级
                    if loop.importance not in ["minor", "major", "critical"]:
                        loop.importance = "minor"

                    new_loops.append(loop)
                    logger.info(f"发现新伏笔: {loop.description[:50]}...")

                except Exception as e:
                    logger.warning(f"解析伏笔数据失败: {e}, 数据: {loop_data}")
                    continue

            logger.info(f"伏笔扫描完成，发现 {len(new_loops)} 个新伏笔")
            return new_loops

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}, 响应: {result_text[:200]}...")
            return []
        except Exception as e:
            logger.error(f"伏笔扫描失败: {e}")
            return []

    async def check_loop_resolution(self, content: str, open_loops: List[PlotLoop]) -> List[str]:
        """
        检查正文是否回收了之前的伏笔

        Args:
            content: 待分析的文本内容
            open_loops: 未解决的伏笔列表

        Returns:
            已解决的伏笔ID列表
        """
        if not open_loops or not content.strip():
            return []

        logger.info(f"正在检查伏笔回收... 待检查伏笔数: {len(open_loops)}")

        # 准备伏笔描述
        loops_text = "\n".join([
            f"{i+1}. [{loop.importance.upper()}] {loop.description}"
            for i, loop in enumerate(open_loops)
        ])

        prompt = f"""
你是一位专业的文学编辑，负责检查小说伏笔的回收情况。

当前待回收的伏笔清单：
{loops_text}

请分析以下文本，看是否解释或解决了上述任何一个伏笔：

【待分析文本】
{content[:4000]}...

【判断标准】
- **完全解决**: 伏笔得到明确解释或结果
- **部分解决**: 伏笔得到部分解释，但仍留有余地
- **未解决**: 伏笔未被提及或解释

请仔细分析每个伏笔是否在文本中得到解决。

返回JSON格式：
{{
    "resolved_loops": [1, 3, 5],  // 已解决的伏笔编号（从1开始）
    "partial_resolved": [2],       // 部分解决的伏笔编号
    "explanations": {{
        "1": "具体如何解决的说明",
        "3": "具体如何解决的说明"
    }}
}}

只返回JSON对象，不要其他说明。
"""

        try:
            result_text = await self.llm.generate(prompt, temperature=0.1)
            result_text = self._clean_json_response(result_text)

            result = json.loads(result_text)

            resolved_indices = result.get("resolved_loops", [])
            if not isinstance(resolved_indices, list):
                resolved_indices = []

            # 转换为伏笔ID列表
            resolved_ids = []
            for idx in resolved_indices:
                if isinstance(idx, int) and 1 <= idx <= len(open_loops):
                    resolved_ids.append(open_loops[idx - 1].id)

            logger.info(f"伏笔回收检查完成，解决 {len(resolved_ids)} 个伏笔")
            return resolved_ids

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}")
            return []
        except Exception as e:
            logger.error(f"伏笔回收检查失败: {e}")
            return []

    async def generate_loops_report(self, project: NovelProject) -> Dict[str, Any]:
        """
        生成伏笔状态报告

        Args:
            project: 小说项目

        Returns:
            伏笔报告
        """
        open_loops = [loop for loop in project.open_loops if loop.status == "open"]
        resolved_loops = project.resolved_loops

        # 按重要性分组统计
        open_by_importance = {
            "critical": len([l for l in open_loops if l.importance == "critical"]),
            "major": len([l for l in open_loops if l.importance == "major"]),
            "minor": len([l for l in open_loops if l.importance == "minor"])
        }

        resolved_by_importance = {
            "critical": len([l for l in resolved_loops if l.importance == "critical"]),
            "major": len([l for l in resolved_loops if l.importance == "major"]),
            "minor": len([l for l in resolved_loops if l.importance == "minor"])
        }

        # 计算解决率
        total_loops = len(open_loops) + len(resolved_loops)
        resolution_rate = len(resolved_loops) / total_loops if total_loops > 0 else 0

        # 生成健康度评估
        health_score = self._calculate_loops_health(open_by_importance, resolution_rate)

        report = {
            "summary": {
                "total_open": len(open_loops),
                "total_resolved": len(resolved_loops),
                "total_loops": total_loops,
                "resolution_rate": round(resolution_rate, 2),
                "health_score": health_score
            },
            "open_by_importance": open_by_importance,
            "resolved_by_importance": resolved_by_importance,
            "critical_issues": self._identify_critical_issues(open_loops),
            "recommendations": self._generate_recommendations(open_by_importance, health_score)
        }

        return report

    def _calculate_loops_health(self, open_by_importance: Dict[str, int], resolution_rate: float) -> float:
        """
        计算伏笔健康度 (0-1, 1为最健康)
        """
        # 基础分数：解决率
        base_score = resolution_rate

        # 惩罚未解决的重要伏笔
        critical_penalty = open_by_importance["critical"] * 0.3
        major_penalty = open_by_importance["major"] * 0.1

        health_score = base_score - critical_penalty - major_penalty
        return max(0.0, min(1.0, health_score))

    def _identify_critical_issues(self, open_loops: List[PlotLoop]) -> List[str]:
        """识别关键问题"""
        issues = []

        critical_loops = [loop for loop in open_loops if loop.importance == "critical"]
        if len(critical_loops) > 2:
            issues.append(f"存在 {len(critical_loops)} 个未解决的关键伏笔")

        # 检查是否有长期未解决的伏笔
        # 这里可以根据创建时间判断

        return issues

    def _generate_recommendations(self, open_by_importance: Dict[str, int], health_score: float) -> List[str]:
        """生成建议"""
        recommendations = []

        if health_score < 0.3:
            recommendations.append("⚠️ 伏笔健康度过低，建议优先解决关键伏笔")
        elif health_score < 0.6:
            recommendations.append("📝 伏笔管理一般，注意及时回收重要线索")

        if open_by_importance["critical"] > 0:
            recommendations.append(f"🔴 有 {open_by_importance['critical']} 个关键伏笔需要优先解决")

        if open_by_importance["major"] > 3:
            recommendations.append("📋 重要伏笔较多，建议规划回收时间表")

        return recommendations

    def _clean_json_response(self, text: str) -> str:
        """清理LLM响应中的JSON部分"""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        # 查找第一个{和最后一个}
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:
            return text[start:end+1]

        # 如果没找到括号，尝试找数组
        start = text.find("[")
        end = text.rfind("]")

        if start != -1 and end != -1 and end > start:
            return text[start:end+1]

        return text