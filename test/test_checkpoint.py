"""
测试断点续创功能
"""
import sys
import os
import asyncio
import tempfile
import shutil

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

async def test_checkpoint_functionality():
    print("Testing Checkpoint Functionality...")

    # Create temporary directory for checkpoints
    temp_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()

    try:
        os.chdir(temp_dir)

        # Initialize components
        llm_client = LiteLLMClient()
        km = MockKnowledgeManager()
        summarizer = MockSummarizer()
        validator = MockValidator()

        orchestrator = NovelAssistantOrchestrator(llm_client, km, summarizer, validator)

        # Test 1: Save checkpoint
        print("1. Testing checkpoint saving...")
        test_state = {
            "user_input": "Test input",
            "task_type": "generate",
            "context": [],
            "core_knowledge": ["test knowledge"],
            "summaries": {},
            "output": "test output",
            "locked_settings": {},
            "validation_result": None,
            "metadata": {"task_id": "test_task"},
            "messages": ["test message"]
        }

        await orchestrator.save_checkpoint(test_state, "test_checkpoint")
        checkpoint_path = "./data/checkpoints/test_checkpoint.pkl"

        if os.path.exists(checkpoint_path):
            print("✅ Checkpoint saved successfully")
        else:
            print("❌ Checkpoint save failed")
            return

        # Test 2: Load checkpoint
        print("2. Testing checkpoint loading...")
        loaded_state = await orchestrator.load_checkpoint("test_checkpoint")

        if loaded_state and loaded_state["user_input"] == "Test input":
            print("✅ Checkpoint loaded successfully")
        else:
            print("❌ Checkpoint load failed")
            return

        # Test 3: Resume from checkpoint
        print("3. Testing resume from checkpoint...")
        result = await orchestrator.process("New input for resumed task", resume_from="test_checkpoint")

        if result and "output" in result:
            print("✅ Resume from checkpoint successful")
        else:
            print("❌ Resume from checkpoint failed")

        print("✅ Checkpoint functionality test completed!")

    finally:
        os.chdir(original_cwd)
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(test_checkpoint_functionality())