"""
测试知识图谱模块
"""
import sys
import os
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.memory.knowledge_graph import KnowledgeGraph, Relation
from core.llm.litellm_client import LiteLLMClient

async def test_knowledge_graph():
    print("Testing KnowledgeGraph...")

    # Mock DB client (in real implementation, this would be a database connection)
    class MockDB:
        def __init__(self):
            self.relations = []

        def execute(self, query, params=None):
            """模拟数据库执行"""
            if "INSERT INTO entity_relations" in query and params:
                self.relations.append({
                    'id': len(self.relations) + 1,
                    'source': params[0],
                    'target': params[1],
                    'relation': params[2],
                    'description': params[3],
                    'created_at': '2024-01-01'
                })

        def fetchall(self, query, params=None):
            """模拟数据库查询"""
            if "SELECT" in query and "entity_relations" in query and params:
                entity_name = params[0]
                return [
                    (r['source'], r['target'], r['relation'], r['description'])
                    for r in self.relations
                    if r['source'] == entity_name or r['target'] == entity_name
                ]
            return []

    db_client = MockDB()
    kg = KnowledgeGraph(db_client)

    # Test adding relations
    await kg.add_relation("Alice", "Bob", "friend_of", "Alice and Bob are close friends")
    await kg.add_relation("Alice", "Ancient Sword", "owns", "Alice possesses the ancient sword")

    print("✅ Added relations to knowledge graph")

    # Test querying relations
    alice_relations = await kg.get_related_entities("Alice")
    print(f"Alice's relations: {len(alice_relations)} found")

    # Test relation extraction from text
    llm_client = LiteLLMClient()
    text = "Alice met Bob in the forest. Bob gave Alice a magical sword. The sword belonged to Bob's father."

    extracted_relations = await kg.extract_relations_from_text(text, llm_client)
    print(f"Extracted relations from text: {len(extracted_relations)} found")

    print("✅ KnowledgeGraph test completed!")

if __name__ == "__main__":
    asyncio.run(test_knowledge_graph())
