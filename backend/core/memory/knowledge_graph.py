"""
简易知识图谱管理
用于管理实体间的关系 (Entity-Relation-Entity)
"""
import json
from typing import List, Dict, Tuple, Optional
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
        # 兼容性处理：如果 db_client 支持 execute
        if hasattr(self.db, "execute"):
            try:
                self.db.execute("""
                CREATE TABLE IF NOT EXISTS entity_relations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    target TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """)
                logger.info("Knowledge graph table initialized")
            except Exception as e:
                logger.warning(f"KG Table init warning: {e}")
        else:
            logger.warning("DB client does not support table initialization")

    async def add_relation(self, source: str, target: str, relation: str, description: str = ""):
        """添加实体关系"""
        logger.info(f"Adding KG relation: {source} -[{relation}]-> {target}")
        # 这里使用参数化查询防止注入，具体语法需根据实际 DB 调整
        query = "INSERT INTO entity_relations (source, target, relation, description) VALUES (?, ?, ?, ?)"
        try:
            # 假设 db_client 有 execute 方法
            if hasattr(self.db, "execute"):
                self.db.execute(query, (source, target, relation, description))
                logger.info("Relation added successfully")
            else:
                logger.warning("DB client does not support SQL execution")
        except Exception as e:
            logger.error(f"Failed to add relation: {e}")

    async def get_related_entities(self, entity_name: str, relation_type: Optional[str] = None) -> List[Relation]:
        """查询相关实体"""
        query = "SELECT source, target, relation, description FROM entity_relations WHERE source = ? OR target = ?"
        params = [entity_name, entity_name]
        
        if relation_type:
            query += " AND relation = ?"
            params.append(relation_type)
            
        try:
            if hasattr(self.db, "fetchall"):
                rows = self.db.fetchall(query, tuple(params))
                relations = [Relation(source=r[0], target=r[1], relation=r[2], description=r[3]) for r in rows]
                logger.info(f"Found {len(relations)} relations for entity: {entity_name}")
                return relations
            return []
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
    {{"source": "实体A", "target": "实体B", "relation": "关系类型(如:父子/盟友/位于)", "description": "简要描述"}}
]
"""
        try:
            # 调用 LLM 并尝试解析 JSON
            result = await llm_client.generate(prompt)
            
            # 简单的 JSON 提取逻辑
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                json_str = result.split("```")[1].split("```")[0].strip()
            else:
                json_str = result

            data = json.loads(json_str)
            
            relations = []
            for item in data:
                relations.append(Relation(
                    source=item.get("source", "Unknown"),
                    target=item.get("target", "Unknown"),
                    relation=item.get("relation", "related_to"),
                    description=item.get("description", "")
                ))
            logger.info(f"Extracted {len(relations)} relations from text")
            return relations
            
        except Exception as e:
            logger.error(f"Relation extraction failed: {e}")
            return []