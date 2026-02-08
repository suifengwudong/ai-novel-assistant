"""
简易知识图谱管理
用于管理实体间的关系 (Entity-Relation-Entity)
"""
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass
from loguru import logger

@dataclass
class Relation:
    source: str
    target: str
    relation: str  # e.g., "friend_of", "located_in", "owns"
    description: str = ""

class KnowledgeGraph:
    def __init__(self, db_client):
        self.db = db_client # 假设复用关系型数据库或图数据库连接
        self._init_table()

    def _init_table(self):
        """初始化关系表"""
        query = """
        CREATE TABLE IF NOT EXISTS entity_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            target TEXT NOT NULL,
            relation TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            self.db.execute(query)
            logger.info("Knowledge graph table initialized")
        except Exception as e:
            logger.warning(f"Failed to init KG table: {e}")

    async def add_relation(self, source: str, target: str, relation: str, description: str = ""):
        """添加实体关系"""
        logger.info(f"Adding relation: {source} -[{relation}]-> {target}")
        query = "INSERT INTO entity_relations (source, target, relation, description) VALUES (?, ?, ?, ?)"
        try:
            self.db.execute(query, (source, target, relation, description))
            logger.info(f"Relation added successfully")
        except Exception as e:
            logger.error(f"Failed to add relation: {e}")

    async def get_related_entities(self, entity_name: str, relation_type: str = None) -> List[Relation]:
        """查询相关实体"""
        if relation_type:
            query = "SELECT source, target, relation, description FROM entity_relations WHERE (source = ? OR target = ?) AND relation = ?"
            params = (entity_name, entity_name, relation_type)
        else:
            query = "SELECT source, target, relation, description FROM entity_relations WHERE source = ? OR target = ?"
            params = (entity_name, entity_name)

        try:
            rows = self.db.fetchall(query, params)
            relations = [Relation(*row) for row in rows]
            logger.info(f"Found {len(relations)} relations for entity: {entity_name}")
            return relations
        except Exception as e:
            logger.error(f"Failed to get relations: {e}")
            return []

    async def extract_relations_from_text(self, text: str, llm_client) -> List[Relation]:
        """使用 LLM 从文本中自动提取关系"""
        prompt = f"""
分析以下文本，提取实体间的关键关系。
文本：{text[:2000]}

返回 JSON 列表格式:
[
    {{"source": "实体A", "target": "实体B", "relation": "父子/朋友/敌对", "description": "简述"}}
]
"""
        try:
            result = await llm_client.generate(prompt)  # Remove format="json" for Ollama
            if isinstance(result, str):
                # 清理可能的 markdown 格式
                result = result.replace("```json", "").replace("```", "").strip()
                data = json.loads(result)
            else:
                data = result

            relations = []
            for item in data:
                relations.append(Relation(
                    source=item.get("source"),
                    target=item.get("target"),
                    relation=item.get("relation"),
                    description=item.get("description", "")
                ))
            logger.info(f"Extracted {len(relations)} relations from text")
            return relations
        except Exception as e:
            logger.error(f"Relation extraction failed: {e}")
            return []