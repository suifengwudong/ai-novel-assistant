"""
测试续写功能
"""
import sys
import os
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.agents.orchestrator import NovelAssistantOrchestrator
from core.llm.litellm_client import LiteLLMClient

# Mock dependencies
class MockKnowledgeManager:
    async def retrieve_context(self, query, top_k=10):
        return ["核心设定：这是一个奇幻世界，只有魔法师才能使用魔法物品。"]

class MockSummarizer:
    async def get_recent_summaries(self, count):
        return []

class MockValidator:
    async def check(self, content, core_knowledge, locked_settings):
        return {"passed": True, "issues": []}

async def test_continue_functionality():
    print("Testing Continue Functionality...")

    # Initialize components
    llm_client = LiteLLMClient()
    km = MockKnowledgeManager()
    summarizer = MockSummarizer()
    validator = MockValidator()

    orchestrator = NovelAssistantOrchestrator(llm_client, km, summarizer, validator)

    # Test continue task type
    print("1. Testing continue task type recognition...")

    # Mock state for continue task
    test_state = {
        "user_input": "请继续写这个故事",
        "task_type": "continue",
        "context": [],
        "core_knowledge": ["核心设定：这是一个奇幻世界，只有魔法师才能使用魔法物品。"],
        "summaries": {},
        "output": "",
        "locked_settings": {},
        "validation_result": None,
        "metadata": {},
        "messages": [],
        "existing_content": "在古老的魔法森林里，年轻的魔法师艾伦发现了一本神秘的魔法书。当他翻开书页时，一道耀眼的光芒闪现而出。"
    }

    # Test intent understanding for continue
    result_state = await orchestrator._understand_intent(test_state)
    print(f"Recognized task type: {result_state['task_type']}")

    # Test content generation for continue
    result_state = await orchestrator._retrieve_context(result_state)
    result_state = await orchestrator._generate_content(result_state)

    if result_state["output"]:
        print("✅ Continue functionality works!")
        print(f"Generated content length: {len(result_state['output'])} characters")
        print(f"First 100 characters: {result_state['output'][:100]}...")
    else:
        print("❌ Continue functionality failed")

    print("✅ Continue functionality test completed!")

if __name__ == "__main__":
    asyncio.run(test_continue_functionality())