"""
节奏分析器
基于字数和情绪曲线，提醒剧情推进
"""
import json
import statistics
from typing import Dict, Any, List, Tuple
from loguru import logger
from backend.core.structure.models import NovelProject, PlotNode, PacingTemplate, PacingCheckpoint

class PacingAnalyzer:
    """
    节奏分析器 - 监控故事节奏和张力

    核心功能：
    1. 分析场景紧张度
    2. 检查全局节奏
    3. 生成节奏建议
    4. 提供进度预警
    """

    def __init__(self, llm_client):
        self.llm = llm_client

        # 预定义的节奏模板
        self.pacing_templates = {
            PacingTemplate.HERO_JOURNEY: [
                PacingCheckpoint(0.05, 2, "普通世界 - 建立现状", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.15, 4, "冒险召唤 - 引入冲突", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.25, 6, "拒绝召唤 - 犹豫挣扎", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.35, 8, "遇到导师 - 获得指引", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.45, 9, "跨越门槛 - 进入冒险", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.55, 10, "考验、盟友、敌人 - 中点危机", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.65, 8, "接近最深处 - 深入敌营", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.75, 9, "严峻考验 - 最大危机", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.85, 7, "奖励 - 获得回报", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.92, 6, "返回之路 - 逃离险境", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(0.98, 8, "复活 - 最终考验", PacingTemplate.HERO_JOURNEY),
                PacingCheckpoint(1.0, 3, "带着宝物归来 - 结局", PacingTemplate.HERO_JOURNEY),
            ],
            PacingTemplate.THREE_ACT: [
                PacingCheckpoint(0.10, 3, "第一幕开头 - 建立世界", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.20, 5, "第一幕发展 - 引入冲突", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.25, 8, "第一幕高潮 - 锁定事件", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.40, 6, "第二幕开头 - 适应新情况", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.50, 7, "第二幕中点 - 重大转折", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.70, 9, "第二幕发展 - 不断升级", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.75, 10, "第二幕高潮 - 黑暗时刻", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.85, 8, "第三幕开头 - 最终推动", PacingTemplate.THREE_ACT),
                PacingCheckpoint(0.95, 9, "第三幕高潮 - 最终对决", PacingTemplate.THREE_ACT),
                PacingCheckpoint(1.0, 4, "第三幕结局 - 解决收尾", PacingTemplate.THREE_ACT),
            ],
            PacingTemplate.SAVE_THE_CAT: [
                PacingCheckpoint(0.05, 3, "开场 - 展示主角生活", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.10, 5, "设置铺垫 - 引入问题", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.15, 7, "主题呈现 - 故事核心", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.20, 8, "铺垫高潮 - 锁定事件", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.25, 6, "第一幕转折 - 进入冒险", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.35, 7, "承诺 - 目标确立", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.50, 8, "中点 - 重大转折", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.55, 6, "坏人逼近 - 压力增加", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.70, 9, "一无所有 - 黑暗时刻", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.75, 7, "灵魂黑夜 - 反思时刻", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.80, 8, "第三幕转折 - 最终推动", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.85, 9, "结局构建 - 高潮铺垫", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(0.95, 10, "最终对决 - 故事高潮", PacingTemplate.SAVE_THE_CAT),
                PacingCheckpoint(1.0, 4, "终场 - 幸福结局", PacingTemplate.SAVE_THE_CAT),
            ]
        }

    async def analyze_scene_tension(self, content: str) -> Dict[str, Any]:
        """
        分析当前场景的紧张度/情绪强度

        Args:
            content: 待分析的场景内容

        Returns:
            包含紧张度分析结果的字典
        """
        logger.info("正在分析场景紧张度...")

        if not content.strip():
            return {
                "tension_score": 5,
                "confidence": 0.0,
                "reason": "内容为空",
                "emotions": []
            }

        prompt = f"""
你是一位专业的文学编辑和叙事分析师。请分析以下场景的紧张度和情绪强度。

【分析维度】
1. **冲突强度**: 人物间的对抗、内部挣扎
2. ** stakes 高度**: 失败的后果严重性
3. **不确定性**: 结果的不确定程度
4. **节奏感**: 场景推进的速度
5. **情绪张力**: 读者的情绪投入度

请给出一个1-10的紧张度评分（1=平静日常，10=生死攸关的巅峰对决）。

场景内容：
{content[:3000]}...

返回JSON格式：
{{
    "tension_score": 7,
    "confidence": 0.85,
    "reason": "具体分析理由",
    "emotions": ["紧张", "期待", "恐惧"],
    "key_elements": ["高风险冲突", "时间压力", "情感投入"]
}}

只返回JSON对象。
"""

        try:
            result_text = await self.llm.generate(prompt, temperature=0.2)
            result_text = self._clean_json_response(result_text)
            result = json.loads(result_text)

            # 验证和标准化结果
            result = self._validate_tension_result(result)

            logger.info(f"场景紧张度分析完成: {result['tension_score']}/10")
            return result

        except Exception as e:
            logger.error(f"场景紧张度分析失败: {e}")
            return self._get_default_tension_result()

    async def check_global_pacing(self, project: NovelProject, current_node: PlotNode) -> Dict[str, Any]:
        """
        检查全局节奏是否符合模板

        Args:
            project: 小说项目
            current_node: 当前正在写作的节点

        Returns:
            节奏检查结果
        """
        logger.info(f"正在检查全局节奏... 项目: {project.title}")

        # 计算当前进度
        current_progress = self._calculate_current_progress(project, current_node)

        # 获取节奏模板
        template = project.pacing_template
        checkpoints = self.pacing_templates.get(template, [])

        if not checkpoints:
            return {
                "status": "unknown",
                "message": f"不支持的节奏模板: {template}",
                "suggestions": []
            }

        # 找到最接近的检查点
        nearest_checkpoint = self._find_nearest_checkpoint(checkpoints, current_progress)

        if not nearest_checkpoint:
            return {
                "status": "normal",
                "message": "当前进度正常",
                "suggestions": []
            }

        # 分析当前紧张度（这里需要实际的场景内容来分析）
        # 暂时使用节点的预估紧张度
        current_tension = getattr(current_node, 'current_tension', 5)

        # 计算偏差
        expected_tension = nearest_checkpoint.expected_tension
        deviation = abs(current_tension - expected_tension)

        # 生成分析结果
        result = self._analyze_pacing_deviation(
            current_progress, current_tension, expected_tension,
            nearest_checkpoint, deviation
        )

        logger.info(f"节奏检查完成 - 进度: {current_progress:.1%}, 紧张度: {current_tension}/10")
        return result

    async def generate_pacing_report(self, project: NovelProject) -> Dict[str, Any]:
        """
        生成完整的节奏分析报告

        Args:
            project: 小说项目

        Returns:
            节奏报告
        """
        logger.info(f"正在生成节奏分析报告... 项目: {project.title}")

        # 计算整体统计
        total_nodes = len(project.outline_tree)
        completed_nodes = sum(1 for node in project.outline_tree
                            if node.status.name == "FINISHED")

        if total_nodes == 0:
            return {"error": "项目没有大纲节点"}

        completion_rate = completed_nodes / total_nodes

        # 分析节奏曲线
        pacing_curve = await self._analyze_pacing_curve(project)

        # 生成建议
        recommendations = self._generate_pacing_recommendations(project, pacing_curve)

        report = {
            "summary": {
                "total_nodes": total_nodes,
                "completed_nodes": completed_nodes,
                "completion_rate": round(completion_rate, 2),
                "current_progress": round(project.completion_percentage, 2)
            },
            "pacing_curve": pacing_curve,
            "template": project.pacing_template.value,
            "recommendations": recommendations,
            "health_score": self._calculate_pacing_health(pacing_curve)
        }

        return report

    def _calculate_current_progress(self, project: NovelProject, current_node: PlotNode) -> float:
        """计算当前进度"""
        if not project.outline_tree:
            return 0.0

        # 找到当前节点的位置
        try:
            current_index = next(i for i, node in enumerate(project.outline_tree)
                               if node.id == current_node.id)
            return (current_index + 1) / len(project.outline_tree)
        except StopIteration:
            return project.completion_percentage

    def _find_nearest_checkpoint(self, checkpoints: List[PacingCheckpoint],
                               progress: float) -> Optional[PacingCheckpoint]:
        """找到最接近的节奏检查点"""
        if not checkpoints:
            return None

        # 找到进度最接近的检查点
        nearest = min(checkpoints, key=lambda cp: abs(cp.position - progress))

        # 只返回相差不超过10%的检查点
        if abs(nearest.position - progress) <= 0.1:
            return nearest

        return None

    def _analyze_pacing_deviation(self, progress: float, current_tension: int,
                                expected_tension: int, checkpoint: PacingCheckpoint,
                                deviation: float) -> Dict[str, Any]:
        """分析节奏偏差"""

        if deviation <= 1:
            return {
                "status": "good",
                "message": f"节奏正常 - {checkpoint.description}",
                "suggestions": []
            }
        elif deviation <= 3:
            return {
                "status": "warning",
                "message": f"节奏略有偏差 - {checkpoint.description} (期望紧张度: {expected_tension}, 当前: {current_tension})",
                "suggestions": [
                    f"考虑调整场景紧张度以符合{checkpoint.description}的要求",
                    "检查是否需要增加或减少冲突元素"
                ]
            }
        else:
            severity = "high" if deviation > 5 else "medium"
            return {
                "status": severity,
                "message": f"节奏严重偏差 - {checkpoint.description} (期望紧张度: {expected_tension}, 当前: {current_tension})",
                "suggestions": [
                    f"⚠️ 当前场景紧张度与{checkpoint.description}相差较大",
                    "建议重新审视场景设计或调整故事节奏",
                    "考虑是否需要修改大纲以适应当前写作方向"
                ]
            }

    async def _analyze_pacing_curve(self, project: NovelProject) -> List[Dict[str, Any]]:
        """分析节奏曲线"""
        curve = []

        for i, node in enumerate(project.outline_tree):
            progress = (i + 1) / len(project.outline_tree)

            # 这里应该分析实际内容，但暂时使用估算值
            estimated_tension = getattr(node, 'estimated_tension', 5)

            curve.append({
                "node_id": node.id,
                "title": node.title,
                "progress": round(progress, 2),
                "tension": estimated_tension,
                "status": node.status.value
            })

        return curve

    def _generate_pacing_recommendations(self, project: NovelProject,
                                       pacing_curve: List[Dict[str, Any]]) -> List[str]:
        """生成节奏建议"""
        recommendations = []

        if not pacing_curve:
            return ["无法生成节奏建议：缺少节奏数据"]

        # 检查是否有明显的节奏问题
        tensions = [point["tension"] for point in pacing_curve]

        if len(tensions) > 1:
            # 检查波动是否过大
            if statistics.stdev(tensions) > 3:
                recommendations.append("⚠️ 故事节奏波动较大，建议平滑化紧张度曲线")

            # 检查是否有连续低潮
            low_tension_streaks = self._find_low_tension_streaks(tensions)
            if low_tension_streaks:
                recommendations.append(f"发现 {len(low_tension_streaks)} 处连续低潮段落，建议增加冲突")

        # 根据模板给出建议
        template = project.pacing_template
        if template == PacingTemplate.HERO_JOURNEY:
            recommendations.append("💡 英雄之旅模板：确保中点有重大转折，高潮前有低谷")
        elif template == PacingTemplate.THREE_ACT:
            recommendations.append("💡 三幕结构：第一幕建立冲突，第二幕升级矛盾，第三幕解决收尾")

        return recommendations

    def _find_low_tension_streaks(self, tensions: List[int]) -> List[Tuple[int, int]]:
        """查找连续低潮段落"""
        streaks = []
        start = -1

        for i, tension in enumerate(tensions):
            if tension <= 3:  # 低潮阈值
                if start == -1:
                    start = i
            elif start != -1:
                if i - start >= 3:  # 连续3个或以上
                    streaks.append((start, i-1))
                start = -1

        # 处理结尾
        if start != -1 and len(tensions) - start >= 3:
            streaks.append((start, len(tensions)-1))

        return streaks

    def _calculate_pacing_health(self, pacing_curve: List[Dict[str, Any]]) -> float:
        """计算节奏健康度"""
        if not pacing_curve:
            return 0.0

        # 基于波动性和合理性的简单评分
        tensions = [point["tension"] for point in pacing_curve]

        if len(tensions) < 2:
            return 0.8  # 太少数据，给个中等分数

        # 计算波动性（波动太大会降低分数）
        try:
            std_dev = statistics.stdev(tensions)
            volatility_penalty = min(std_dev / 5, 0.5)  # 波动每增加1点扣0.1分
        except:
            volatility_penalty = 0

        # 基础分数
        base_score = 0.8

        health_score = base_score - volatility_penalty
        return max(0.0, min(1.0, health_score))

    def _validate_tension_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """验证紧张度分析结果"""
        defaults = {
            "tension_score": 5,
            "confidence": 0.5,
            "reason": "分析完成",
            "emotions": [],
            "key_elements": []
        }

        for key, default_value in defaults.items():
            if key not in result:
                result[key] = default_value

        # 验证分数范围
        if not isinstance(result["tension_score"], (int, float)):
            result["tension_score"] = 5
        result["tension_score"] = max(1, min(10, int(result["tension_score"])))

        if not isinstance(result["confidence"], (int, float)):
            result["confidence"] = 0.5
        result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))

        return result

    def _get_default_tension_result(self) -> Dict[str, Any]:
        """获取默认紧张度结果"""
        return {
            "tension_score": 5,
            "confidence": 0.0,
            "reason": "分析失败，使用默认值",
            "emotions": [],
            "key_elements": []
        }

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

        return text