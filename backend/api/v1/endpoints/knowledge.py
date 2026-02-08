from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from core.dependencies import container

router = APIRouter()

class KnowledgeItem(BaseModel):
    content: str
    category: str = "general"
    metadata: Optional[dict] = None

def get_vector_store():
    return container.vector_store

def get_knowledge_graph():
    return container.knowledge_graph

@router.post("/add")
async def add_knowledge(
    item: KnowledgeItem,
    vector_store=Depends(get_vector_store)
):
    """添加知识条目"""
    try:
        # 生成唯一ID
        import uuid
        doc_id = str(uuid.uuid4())

        # 添加到向量存储
        await vector_store.add_texts(
            texts=[item.content],
            metadatas=[{
                "category": item.category,
                **(item.metadata or {})
            }],
            ids=[doc_id]
        )

        # 如果是实体关系，也添加到知识图谱
        if item.category == "relation":
            # 这里可以解析关系并添加到知识图谱
            pass

        return {"status": "success", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add knowledge: {str(e)}")

@router.get("/retrieve")
async def retrieve_knowledge(
    query: str,
    top_k: int = 5,
    category: Optional[str] = None
):
    """检索知识"""
    try:
        # 暂时返回mock数据
        return {
            "results": [
                {"content": f"关于 {query} 的相关背景知识...", "score": 0.92}
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve knowledge: {str(e)}")

@router.post("/relation")
async def add_relation(
    source: str,
    target: str,
    relation: str,
    description: str = "",
    knowledge_graph=Depends(get_knowledge_graph)
):
    """添加实体关系"""
    try:
        await knowledge_graph.add_relation(source, target, relation, description)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add relation: {str(e)}")

@router.get("/relations/{entity}")
async def get_entity_relations(
    entity: str,
    relation_type: Optional[str] = None,
    knowledge_graph=Depends(get_knowledge_graph)
):
    """获取实体的所有关系"""
    try:
        relations = await knowledge_graph.get_related_entities(entity, relation_type)
        return {"relations": [r.__dict__ for r in relations]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get relations: {str(e)}")