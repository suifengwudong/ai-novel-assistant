"""
大纲守卫 Agent
负责监控正文写作是否偏离预设大纲
"""
import json
from typing import Dict, Any, Optional
from loguru import logger
from backend.core.structure.models import PlotNode, NodeStatus

class OutlineGuardian:
    """
    大纲守卫 - 实时监控写作偏离度

    核心功能：
    1. 对比预设大纲与实际正文
    2. 计算偏离度评分
    3. 提供修正建议
    4. 支持大纲自动更新
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    async def check_deviation(self, outline_node: PlotNode, actual_content: str) -> Dict[str, Any]:
        """
        检查正文是否偏离大纲

        Args:
            outline_node: 大纲节点
            actual_content: 实际写作内容

        Returns:
            包含偏离分析结果的字典
        """
        logger.info(f"正在进行大纲偏离度检查... 节点: {outline_node.title}")

        if not outline_node.description.strip():
            logger.warning("大纲节点描述为空，跳过偏离检查")
            return {
                "is_deviated": False,
                "deviation_score": 0.0,
                "reason": "大纲描述为空",
                "impact_analysis": "无影响",
                "suggestion": "请完善大纲描述"
            }

        prompt = f"""
你是一名严格的主编和小说的结构化写作专家。请对比【预设大纲】和【实际正文】，判断剧情走向是否发生重大偏移。

【预设大纲】
标题: {outline_node.title}
类型: {outline_node.type.value}
描述: {outline_node.description}

【实际正文】(已写作内容)
{actual_content[:4000]}...

请从以下维度分析偏离情况：

1. **核心冲突结果**: 预设的冲突结局是否达成？
2. **关键人物命运**: 主要角色的命运走向是否符合预期？
3. **剧情逻辑**: 这里的改动是否会破坏后续剧情的逻辑链？
4. **主题一致性**: 是否偏离了故事的核心主题？
5. **节奏影响**: 是否影响了整体故事节奏？

请以专业、建设性的方式分析，并提供具体的修改建议。

返回 JSON 格式:
{{
    "is_deviated": true/false,           // 是否存在重大偏离
    "deviation_score": 0.0-1.0,         // 偏离度评分 (0完全一致，1完全无关)
    "reason": "简述主要偏移原因",       // 具体说明哪里偏离了
    "impact_analysis": "如果不修正，会对后续造成什么影响",  // 影响评估
    "suggestion": "具体修改建议，可以包括修改正文或调整大纲",  // 建设性建议
    "severity": "low/medium/high",      // 严重程度
    "recommendation_type": "fix_content/update_outline/accept_change"  // 建议类型
}}
"""

        try:
            result_text = await self.llm.generate(prompt, temperature=0.3)

            # 清理和解析JSON
            result_text = self._clean_json_response(result_text)
            result = json.loads(result_text)

            # 验证和标准化结果
            result = self._validate_guardian_result(result)

            # 更新节点状态
            outline_node.deviation_score = result["deviation_score"]
            outline_node.actual_content_summary = self._generate_content_summary(actual_content)

            logger.info(f"偏离检查完成 - 节点: {outline_node.title}, 偏离度: {result['deviation_score']:.2f}")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {e}, 原始响应: {result_text[:500]}...")
            return self._get_fallback_result()
        except Exception as e:
            logger.error(f"Guardian check failed: {e}")
            return self._get_fallback_result()

    async def auto_update_outline(self, project, node_id: str, new_summary: str) -> Dict[str, Any]:
        """
        如果用户决定保留偏移（"园丁剪枝"），则自动更新后续大纲

        Args:
            project: 小说项目对象
            node_id: 当前节点ID
            new_summary: 新的内容总结

        Returns:
            更新建议
        """
        logger.info(f"正在生成大纲更新建议... 节点: {node_id}")

        current_node = project.get_node_by_id(node_id)
        if not current_node:
            return {"success": False, "error": "节点不存在"}

        # 获取后续节点
        subsequent_nodes = self._get_subsequent_nodes(project, node_id)

        if not subsequent_nodes:
            return {"success": True, "message": "没有后续节点需要更新"}

        prompt = f"""
基于当前节点的实际写作结果，分析对后续大纲的影响并提出更新建议。

【当前节点】
标题: {current_node.title}
原始大纲: {current_node.description}
实际结果: {new_summary}

【后续节点大纲】
{chr(10).join([f"- {node.title}: {node.description}" for node in subsequent_nodes])}

请分析：
1. 当前节点的实际结果如何影响后续剧情？
2. 哪些后续节点需要调整？
3. 具体应该如何修改？

返回 JSON:
{{
    "affected_nodes": ["node_id1", "node_id2"],
    "update_suggestions": [
        {{
            "node_id": "node_id",
            "original_outline": "原大纲",
            "suggested_outline": "建议修改后的大纲",
            "reason": "修改原因"
        }}
    ],
    "overall_impact": "整体影响评估"
}}
"""

        try:
            result_text = await self.llm.generate(prompt, temperature=0.4)
            result = json.loads(self._clean_json_response(result_text))

            logger.info(f"大纲更新建议生成完成，影响 {len(result.get('affected_nodes', []))} 个节点")
            return {"success": True, "data": result}

        except Exception as e:
            logger.error(f"Auto update outline failed: {e}")
            return {"success": False, "error": str(e)}

    def _get_subsequent_nodes(self, project, node_id: str) -> list:
        """获取后续节点（简化版，实际应该考虑树状结构）"""
        nodes = project.outline_tree
        start_idx = next((i for i, node in enumerate(nodes) if node.id == node_id), -1)

        if start_idx == -1:
            return []

        return nodes[start_idx + 1:]

    def _generate_content_summary(self, content: str) -> str:
        """生成内容总结（简化版）"""
        if len(content) <= 200:
            return content
        return content[:200] + "..."

    def _clean_json_response(self, text: str) -> str:
        """清理LLM响应中的JSON部分"""
        # 移除可能的markdown代码块标记
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

        return text

    def _validate_guardian_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证和标准化检查结果"""
        # 确保必要字段存在
        defaults = {
            "is_deviated": False,
            "deviation_score": 0.0,
            "reason": "检查完成",
            "impact_analysis": "无明显影响",
            "suggestion": "继续写作",
            "severity": "low",
            "recommendation_type": "accept_change"
        }

        for key, default_value in defaults.items():
            if key not in result:
                result[key] = default_value

        # 验证数值范围
        if not isinstance(result["deviation_score"], (int, float)):
            result["deviation_score"] = 0.0
        result["deviation_score"] = max(0.0, min(1.0, float(result["deviation_score"])))

        # 验证枚举值
        if result["severity"] not in ["low", "medium", "high"]:
            result["severity"] = "low"

        if result["recommendation_type"] not in ["fix_content", "update_outline", "accept_change"]:
            result["recommendation_type"] = "accept_change"

        return result

    def _get_fallback_result(self) -> Dict[str, Any]:
        """获取默认结果（当检查失败时）"""
        return {
            "is_deviated": False,
            "deviation_score": 0.0,
            "reason": "检查失败，使用默认结果",
            "impact_analysis": "无法评估",
            "suggestion": "请手动检查",
            "severity": "low",
            "recommendation_type": "accept_change"
        }