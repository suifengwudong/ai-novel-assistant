from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Any
from core.dependencies import container

router = APIRouter()

class CheckDeviationRequest(BaseModel):
    outline_title: str
    outline_desc: str
    content: str

def get_outline_guardian():
    return container.outline_guardian

@router.post("/check_deviation")
async def check_deviation(
    request: CheckDeviationRequest,
    guardian=Depends(get_outline_guardian)
):
    """
    检查正文与大纲的偏离度
    """
    try:
        # 构造临时节点对象用于检查
        from core.structure.models import PlotNode, NodeType

        # 临时创建一个节点对象
        temp_node = PlotNode(
            id="temp",
            title=request.outline_title,
            description=request.outline_desc,
            type=NodeType.CHAPTER
        )

        result = await guardian.check_deviation(temp_node, request.content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deviation check failed: {str(e)}")

class LogicValidationRequest(BaseModel):
    content: str
    core_knowledge: List[str]
    locked_settings: Optional[dict] = None

def get_logic_validator():
    return container.logic_validator

@router.post("/validate_logic")
async def validate_logic(
    request: LogicValidationRequest,
    validator=Depends(get_logic_validator)
):
    """
    验证内容逻辑一致性
    """
    try:
        result = await validator.check(
            content=request.content,
            core_knowledge=request.core_knowledge,
            locked_settings=request.locked_settings or {}
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logic validation failed: {str(e)}")