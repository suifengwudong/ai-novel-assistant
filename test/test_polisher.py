"""
测试润色优化Agent
"""
import sys
import os
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.agents.polisher import PolishingAgent
from core.llm.litellm_client import LiteLLMClient

async def test_polishing_agent():
    print("Testing Polishing Agent...")

    llm_client = LiteLLMClient()
    polisher = PolishingAgent(llm_client)

    # Test content to polish
    original_content = """
    艾丽丝走进森林。森林很暗。她的心跳很快。她看到一只狼。狼很大。艾丽丝害怕但她拿着剑。剑很重。她挥剑打狼。狼跑了。艾丽丝松了口气。
    """

    print("1. Testing general polishing...")
    try:
        polished = await polisher.polish(original_content, "general")
        print("✅ General polishing completed")
        print(f"Original length: {len(original_content)}")
        print(f"Polished length: {len(polished)}")
        print(f"Preview: {polished[:200]}...")
    except Exception as e:
        print(f"❌ General polishing failed: {e}")
        return

    print("2. Testing descriptive polishing...")
    try:
        polished_desc = await polisher.polish(original_content, "descriptive")
        print("✅ Descriptive polishing completed")
        print(f"Preview: {polished_desc[:200]}...")
    except Exception as e:
        print(f"❌ Descriptive polishing failed: {e}")

    print("3. Testing action polishing...")
    try:
        polished_action = await polisher.polish(original_content, "action")
        print("✅ Action polishing completed")
        print(f"Preview: {polished_action[:200]}...")
    except Exception as e:
        print(f"❌ Action polishing failed: {e}")

    print("✅ Polishing Agent test completed!")

if __name__ == "__main__":
    asyncio.run(test_polishing_agent())