"""
逻辑校验引擎
检测生成内容与核心设定、上下文的一致性
"""
from typing import List, Dict, Any
from loguru import logger

class LogicValidator:
    def __init__(self, llm_client):
        self.llm = llm_client

    async def check(
        self, 
        content: str, 
        core_knowledge: List[str], 
        locked_settings: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        校验内容逻辑
        
        Args:
            content: 待校验的生成内容
            core_knowledge: 检索到的核心知识（世界观、人物设定）
            locked_settings: 必须遵守的锁定设定
            
        Returns:
            Dict: { "passed": bool, "issues": List[str], "suggestions": List[str] }
        """
        logger.info("正在执行逻辑校验...")
        
        prompt = f"""
请作为一名严谨的小说逻辑编辑，检查以下内容是否与设定冲突。

【核心设定】
{self._format_list(core_knowledge)}

【锁定设定】（绝对不可违背）
{self._format_dict(locked_settings)}

【待校验内容】
{content}

请检查：
1. 人物行为是否符合性格设定？
2. 是否违背了世界观的基础规则？
3. 是否与锁定设定产生直接冲突？
4. 时间线和因果逻辑是否通顺？

返回 JSON 格式：
{{
    "passed": true/false,
    "issues": ["冲突点1", "冲突点2"],
    "suggestions": ["修改建议1", "修改建议2"]
}}
"""
        try:
            result = await self.llm.generate(prompt)  # Remove format="json" for Ollama compatibility
            # 假设 llm.generate 在 format="json" 时返回字典，如果是字符串需自行解析
            if isinstance(result, str):
                import json
                # 简单的清理 markdown 代码块标记
                cleaned = result.replace("```json", "").replace("```", "").strip()
                try:
                    parsed = json.loads(cleaned)
                    return parsed
                except json.JSONDecodeError:
                    # 如果JSON解析失败，尝试提取有用信息
                    logger.warning(f"JSON解析失败，原始响应: {cleaned}")
                    # 简单启发式：检查是否包含"false"或问题描述
                    if "false" in cleaned.lower() or "冲突" in cleaned or "问题" in cleaned:
                        return {
                            "passed": False,
                            "issues": ["内容存在逻辑问题"],
                            "suggestions": ["请检查内容逻辑一致性"]
                        }
                    else:
                        return {
                            "passed": True,
                            "issues": [],
                            "suggestions": []
                        }
            return result
            
        except Exception as e:
            logger.error(f"Logic validation failed: {e}")
            # 降级策略：如果校验出错，默认通过，但记录警告
            return {
                "passed": True,
                "issues": [f"校验服务异常: {str(e)}"],
                "suggestions": []
            }

    def _format_list(self, items: List[str]) -> str:
        if not items: return "无"
        return "\n".join([f"- {item}" for item in items])

    def _format_dict(self, data: Dict) -> str:
        if not data: return "无"
        return "\n".join([f"- {k}: {v}" for k, v in data.items()])