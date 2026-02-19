"""
风格学习 API 路由
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from loguru import logger

from core.style_learning import StyleLearner
from core.llm.litellm_client import LiteLLMClient

router = APIRouter(prefix="/style", tags=["style"])


class StyleAnalyzeRequest(BaseModel):
    sample_text: str
    style_name: str


@router.post("/analyze")
async def analyze_style(request: StyleAnalyzeRequest):
    """分析文本风格，生成风格画像"""
    if not request.sample_text.strip():
        raise HTTPException(status_code=400, detail="样章内容不能为空")
    if not request.style_name.strip():
        raise HTTPException(status_code=400, detail="风格名称不能为空")

    try:
        llm_client = LiteLLMClient()
        learner = StyleLearner(llm_client, db=None)
        profile = await learner.analyze_style(request.sample_text, request.style_name)
        return profile.to_dict()
    except Exception as e:
        logger.error(f"Style analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"风格分析失败: {str(e)}")
