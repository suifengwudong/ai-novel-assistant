from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from core.dependencies import container

router = APIRouter()

class GenRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 4096

def get_llm_client():
    return container.llm_client

@router.post("/chapter")
async def generate_chapter(
    req: GenRequest,
    llm=Depends(get_llm_client)
):
    """
    生成章节内容
    """
    try:
        content = await llm.generate(
            prompt=req.prompt,
            temperature=req.temperature,
            max_tokens=req.max_tokens
        )
        return {"content": content, "prompt": req.prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

class ContinueRequest(BaseModel):
    existing_content: str
    continuation_prompt: str
    temperature: float = 0.7
    max_tokens: int = 2048

@router.post("/continue")
async def continue_chapter(
    req: ContinueRequest,
    llm=Depends(get_llm_client)
):
    """
    继续生成章节内容
    """
    try:
        # 构建延续提示
        full_prompt = f"{req.existing_content}\n\n继续写作：{req.continuation_prompt}"

        content = await llm.generate(
            prompt=full_prompt,
            temperature=req.temperature,
            max_tokens=req.max_tokens
        )
        return {
            "content": content,
            "existing_content": req.existing_content,
            "continuation_prompt": req.continuation_prompt
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Continuation failed: {str(e)}")