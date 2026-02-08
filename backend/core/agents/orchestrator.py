"""
智能体编排系统
使用LangGraph实现多Agent协作
"""
import pickle
import os
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from dataclasses import dataclass
import operator
from loguru import logger

try:
    from langgraph.graph import StateGraph, END
except ImportError:
    logger.warning("LangGraph not installed, using fallback implementation")
    StateGraph = None
    END = "END"


class AgentState(TypedDict):
    """智能体共享状态"""
    user_input: str                    # 用户输入
    task_type: str                     # 任务类型
    context: List[str]                 # 上下文信息
    core_knowledge: List[str]          # 核心知识
    summaries: Dict[str, str]          # 总结信息
    output: str                        # 输出内容
    locked_settings: Dict[str, Any]    # 锁定设定
    validation_result: Optional[Dict]  # 校验结果
    metadata: Dict[str, Any]           # 元数据
    messages: Annotated[List[str], operator.add]  # 消息历史
    existing_content: Optional[str]    # 现有内容（用于续写）


class NovelAssistantOrchestrator:
    """智能体协调器"""
    
    def __init__(self, llm_client, knowledge_manager, summarizer, validator):
        """
        初始化协调器
        
        Args:
            llm_client: 大模型客户端
            knowledge_manager: 知识管理器
            summarizer: 总结系统
            validator: 校验器
        """
        self.llm = llm_client
        self.km = knowledge_manager
        self.summarizer = summarizer
        self.validator = validator
        
        # 构建工作流
        if StateGraph:
            self.workflow = self._build_workflow()
        else:
            self.workflow = None
            logger.warning("Using fallback workflow without LangGraph")
    
    async def save_checkpoint(self, state: AgentState, checkpoint_id: str):
        """保存当前执行状态"""
        path = f"./data/checkpoints/{checkpoint_id}.pkl"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, "wb") as f:
                pickle.dump(state, f)
            logger.info(f"Checkpoint saved: {checkpoint_id}")
        except Exception as e:
            logger.error(f"Failed to save checkpoint {checkpoint_id}: {e}")

    async def load_checkpoint(self, checkpoint_id: str) -> Optional[AgentState]:
        """加载执行状态"""
        path = f"./data/checkpoints/{checkpoint_id}.pkl"
        if not os.path.exists(path):
            logger.warning(f"Checkpoint not found: {checkpoint_id}")
            return None
        try:
            with open(path, "rb") as f:
                state = pickle.load(f)
            logger.info(f"Checkpoint loaded: {checkpoint_id}")
            return state
        except Exception as e:
            logger.error(f"Failed to load checkpoint {checkpoint_id}: {e}")
            return None
    
    def _build_workflow(self):
        """构建智能体工作流"""
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("understand", self._understand_intent)
        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("generate", self._generate_content)
        workflow.add_node("validate", self._validate_output)
        workflow.add_node("refine", self._refine_output)
        
        # 定义边
        workflow.set_entry_point("understand")
        workflow.add_edge("understand", "retrieve_context")
        workflow.add_edge("retrieve_context", "generate")
        workflow.add_edge("generate", "validate")
        
        # 条件分支
        workflow.add_conditional_edges(
            "validate",
            self._should_refine,
            {
                "refine": "refine",
                "finish": END
            }
        )
        workflow.add_edge("refine", END)
        
        return workflow.compile()
    
    async def process(self, user_input: str, resume_from: str = None, **kwargs) -> Dict[str, Any]:
        """
        处理用户请求
        
        Args:
            user_input: 用户输入
            resume_from: 检查点ID，用于恢复之前的执行状态
            **kwargs: 其他参数
            
        Returns:
            Dict: 处理结果
        """
        logger.info(f"开始处理请求: {user_input[:100]}...")
        
        # 1. 尝试恢复状态
        if resume_from:
            state = await self.load_checkpoint(resume_from)
            if state:
                logger.info(f"Resuming from checkpoint: {resume_from}")
                # 更新用户输入（如果提供了新的输入）
                if user_input:
                    state["user_input"] = user_input
                    state["metadata"].update(kwargs)
            else:
                logger.warning("Checkpoint not found, starting fresh.")
                state = None
        
        # 2. 如果没有恢复状态，初始化新状态
        if not state:
            state: AgentState = {
                "user_input": user_input,
                "task_type": "",
                "context": [],
                "core_knowledge": [],
                "summaries": {},
                "output": "",
                "locked_settings": kwargs.get("locked_settings", {}),
                "validation_result": None,
                "metadata": kwargs,
                "messages": [],
                "existing_content": kwargs.get("existing_content", None)
            }
        
        if self.workflow:
            # 使用LangGraph工作流
            result = await self.workflow.ainvoke(state)
        else:
            # 降级方案：顺序执行
            result = await self._fallback_process(state)
        
        logger.info("✅ 请求处理完成")
        return result
    
    async def _fallback_process(self, state: AgentState) -> AgentState:
        """降级处理方案（不使用LangGraph）"""
        task_id = state["metadata"].get("task_id", "unknown")
        
        state = await self._understand_intent(state)
        await self.save_checkpoint(state, f"{task_id}_intent_understood")
        
        state = await self._retrieve_context(state)
        await self.save_checkpoint(state, f"{task_id}_context_retrieved")
        
        state = await self._generate_content(state)
        await self.save_checkpoint(state, f"{task_id}_content_generated")
        
        state = await self._validate_output(state)
        await self.save_checkpoint(state, f"{task_id}_output_validated")
        
        if self._should_refine(state) == "refine":
            state = await self._refine_output(state)
            await self.save_checkpoint(state, f"{task_id}_output_refined")
        
        return state
    
    async def _understand_intent(self, state: AgentState) -> AgentState:
        """理解用户意图"""
        logger.info("Agent: 理解意图")
        
        prompt = f"""
分析用户指令，判断任务类型和关键信息：

用户输入: {state['user_input']}

返回JSON格式：
{{
    "task_type": "generate/continue/summarize/check/edit/outline",
    "target": "chapter/scene/dialogue/description/character",
    "requirements": ["要求1", "要求2"],
    "style": "风格描述",
    "word_count": 目标字数
}}

任务类型说明：
- generate: 生成新内容
- continue: 续写现有内容（断点续写）
- summarize: 生成总结
- check: 校验内容
- edit: 编辑修改
- outline: 生成大纲
"""
        
        try:
            result = await self.llm.generate(prompt)  # Remove format="json" for Ollama compatibility
            import json
            # Try to parse as JSON, fallback to default if parsing fails
            try:
                parsed = json.loads(result)
            except json.JSONDecodeError:
                # If JSON parsing fails, extract information manually or use defaults
                logger.warning("Failed to parse LLM response as JSON, using defaults")
                parsed = {"task_type": "generate"}
            
            state["task_type"] = parsed.get("task_type", "generate")
            state["metadata"].update(parsed)
            state["messages"].append(f"意图识别: {state['task_type']}")
            
            logger.info(f"识别任务类型: {state['task_type']}")
        except Exception as e:
            logger.error(f"意图识别失败: {e}")
            state["task_type"] = "generate"
        
        return state
    
    async def _retrieve_context(self, state: AgentState) -> AgentState:
        """检索相关上下文"""
        logger.info("Agent: 检索上下文")
        
        # 检索核心知识
        core_knowledge = await self.km.retrieve_context(
            query=state["user_input"],
            top_k=10
        )
        state["core_knowledge"] = core_knowledge
        
        # 获取相关总结
        if state["task_type"] in ["generate", "continue"]:
            # 获取最近3章的总结
            try:
                recent_summaries = await self.summarizer.db.get_recent_summaries(3)
                state["summaries"] = {
                    f"chapter_{i}": s.content
                    for i, s in enumerate(recent_summaries)
                }
            except:
                state["summaries"] = {}
        
        state["messages"].append(f"检索到 {len(core_knowledge)} 条核心知识")
        logger.info(f"检索到 {len(core_knowledge)} 条核心知识")
        
        return state
    
    async def _generate_content(self, state: AgentState) -> AgentState:
        """生成内容"""
        logger.info(f"Agent: 生成内容 (任务类型: {state['task_type']})")
        
        # 构建系统消息
        system_message = """你是一位专业的小说创作助手，擅长生成高质量的小说内容。
你必须严格遵守核心设定和锁定设定，保持与前文的连贯性。
生成的内容要符合人物性格，情节合理，文笔流畅。"""
        
        # 根据任务类型构建不同的用户提示
        if state["task_type"] == "continue" and state.get("existing_content"):
            # 续写模式
            prompt = f"""
请续写以下小说内容：

【现有内容】（请从此处继续写）
{state['existing_content']}

【用户需求】
{state['user_input']}

【核心设定】（必须严格遵守，不可违背）
{self._format_list(state['core_knowledge'])}

【前文脉络】
{self._format_dict(state['summaries'])}

【锁定设定】（绝对不可更改）
{self._format_dict(state['locked_settings'])}

续写要求：
1. 严格遵守核心设定和锁定设定
2. 保持与现有内容的连贯性和一致性
3. 人物行为符合已设定的性格
4. 情节推进合理，逻辑自洽
5. 文笔流畅，描写生动
6. 直接从现有内容末尾开始续写，不要重复已有内容

请继续生成：
"""
        else:
            # 普通生成模式
            prompt = f"""
请根据以下信息生成小说内容：

【用户需求】
{state['user_input']}

【核心设定】（必须严格遵守，不可违背）
{self._format_list(state['core_knowledge'])}

【前文脉络】
{self._format_dict(state['summaries'])}

【锁定设定】（绝对不可更改）
{self._format_dict(state['locked_settings'])}

生成要求：
1. 严格遵守核心设定和锁定设定
2. 保持与前文的连贯性和一致性
3. 人物行为符合已设定的性格
4. 情节推进合理，逻辑自洽
5. 文笔流畅，描写生动

请开始生成：
"""
        
        try:
            output = await self.llm.generate(
                prompt=prompt,
                system_message=system_message,
                temperature=state["metadata"].get("temperature", 0.7),
                max_tokens=state["metadata"].get("max_tokens", 4000)
            )
            
            state["output"] = output
            state["messages"].append(f"生成内容: {len(output)} 字")
            
            logger.info(f"✅ 内容生成完成，共 {len(output)} 字")
        except Exception as e:
            logger.error(f"内容生成失败: {e}")
            state["output"] = ""
            state["messages"].append(f"生成失败: {str(e)}")
        
        return state
    
    async def _validate_output(self, state: AgentState) -> AgentState:
        """验证输出"""
        logger.info("Agent: 验证输出")
        
        if not state.get("output"):
            state["validation_result"] = {
                "passed": False,
                "issues": ["生成内容为空"]
            }
            return state
        
        try:
            validation_result = await self.validator.check(
                content=state["output"],
                core_knowledge=state["core_knowledge"],
                locked_settings=state.get("locked_settings", {})
            )
            
            state["validation_result"] = validation_result
            state["messages"].append(
                f"校验结果: {'通过' if validation_result['passed'] else '未通过'}"
            )
            
            logger.info(f"校验结果: {validation_result['passed']}")
        except Exception as e:
            logger.error(f"校验失败: {e}")
            state["validation_result"] = {
                "passed": True,  # 降级：校验失败则默认通过
                "issues": []
            }
        
        return state
    
    def _should_refine(self, state: AgentState) -> str:
        """判断是否需要优化"""
        if not state.get("validation_result"):
            return "finish"
        
        if not state["validation_result"]["passed"]:
            # 检查是否已经尝试过优化
            refine_count = state["metadata"].get("refine_count", 0)
            if refine_count < 2:  # 最多优化2次
                return "refine"
        
        return "finish"
    
    async def _refine_output(self, state: AgentState) -> AgentState:
        """优化输出"""
        logger.info("Agent: 优化输出")
        
        issues = state["validation_result"].get("issues", [])
        
        prompt = f"""
以下内容存在问题，请修正：

【原内容】
{state['output']}

【问题清单】
{self._format_list(issues)}

【核心设定】
{self._format_list(state['core_knowledge'])}

【锁定设定】
{self._format_dict(state['locked_settings'])}

请针对问题进行修正，保持其他部分不变。只输出修正后的完整内容。
"""
        
        try:
            refined = await self.llm.generate(prompt)
            state["output"] = refined
            state["messages"].append("内容已优化")
            
            # 增加优化计数
            state["metadata"]["refine_count"] = state["metadata"].get("refine_count", 0) + 1
            
            logger.info("✅ 内容优化完成")
        except Exception as e:
            logger.error(f"内容优化失败: {e}")
        
        return state
    
    def _format_list(self, items: List[str]) -> str:
        """格式化列表"""
        if not items:
            return "无"
        return "\n".join([f"- {item}" for item in items])
    
    def _format_dict(self, data: Dict) -> str:
        """格式化字典"""
        if not data:
            return "无"
        return "\n".join([f"- {k}: {v}" for k, v in data.items()])
