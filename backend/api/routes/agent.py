"""
智能体 API 路由
包含润色、读者反馈模拟、流式生成等功能
"""
import json
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from loguru import logger
from pydantic import BaseModel

from core.agents.polisher import PolishingAgent
from core.feedback_simulator import FeedbackSimulator, ReaderType
from core.llm.litellm_client import LiteLLMClient

router = APIRouter(prefix="/agent", tags=["agent"])


# ============================
# 请求/响应模型
# ============================


class PolishRequest(BaseModel):
    content: str
    focus: str = "general"


class FeedbackRequest(BaseModel):
    content: str
    reader_types: List[str]


class GenerateRequest(BaseModel):
    prompt: str
    system_message: Optional[str] = None
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 4000


# ============================
# 路由处理器
# ============================


@router.post("/polish")
async def polish_content(request: PolishRequest):
    """对文本进行智能润色"""
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="内容不能为空")

    valid_focus = {"general", "descriptive", "emotional", "action"}
    if request.focus not in valid_focus:
        raise HTTPException(status_code=400, detail=f"无效的润色侧重点，可选: {valid_focus}")

    try:
        llm_client = LiteLLMClient()
        polisher = PolishingAgent(llm_client)
        result = await polisher.polish(request.content, request.focus)
        return {"result": result}
    except Exception as e:
        logger.error(f"Polishing failed: {e}")
        raise HTTPException(status_code=500, detail=f"润色失败: {str(e)}")


@router.post("/feedback")
async def simulate_feedback(request: FeedbackRequest):
    """模拟不同类型读者的反馈"""
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="内容不能为空")

    # 过滤有效的读者类型
    valid_types = {rt.value for rt in ReaderType}
    reader_types = [ReaderType(rt) for rt in request.reader_types if rt in valid_types]
    if not reader_types:
        raise HTTPException(status_code=400, detail=f"无效的读者类型，可选: {valid_types}")

    try:
        llm_client = LiteLLMClient()
        simulator = FeedbackSimulator(llm_client)
        result = await simulator.simulate_feedback(request.content, reader_types)
        return result
    except Exception as e:
        logger.error(f"Feedback simulation failed: {e}")
        raise HTTPException(status_code=500, detail=f"反馈模拟失败: {str(e)}")


@router.post("/generate/stream")
async def generate_stream(request: GenerateRequest):
    """
    流式生成文本 (Server-Sent Events)

    客户端接收格式:
      data: {"content": "文本片段"}\n\n
      data: [DONE]\n\n
    """
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt 不能为空")

    llm_client = LiteLLMClient()

    async def event_generator():
        try:
            async for chunk in llm_client.generate_stream(
                prompt=request.prompt,
                system_message=request.system_message,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.error(f"Streaming generation error: {e}")
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        finally:
            yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
