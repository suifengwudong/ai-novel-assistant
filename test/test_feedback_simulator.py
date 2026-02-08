"""
测试读者反馈模拟器
"""
import sys
import os
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.feedback_simulator import FeedbackSimulator, ReaderType
from core.llm.litellm_client import LiteLLMClient

async def test_feedback_simulator():
    print("Testing Feedback Simulator...")

    llm_client = LiteLLMClient()
    simulator = FeedbackSimulator(llm_client)

    # Test content
    test_content = """
    艾丽丝终于找到了那把传说中的古剑。剑柄上镶嵌着神秘的符文，剑身闪烁着蓝色的光芒。
    她握紧剑柄的那一刻，一股暖流涌入她的身体。突然，她发现自己竟然变得隐形了！

    "太神奇了！"艾丽丝兴奋地自语道。

    她悄悄绕过守卫，潜入城堡深处。守卫们毫无察觉地走来走去，完全不知道危险已经降临。
    """

    print("1. Testing single reader type feedback...")
    try:
        feedback = await simulator.simulate_feedback(test_content, [ReaderType.CASUAL])
        print("✅ Single reader feedback generated")
        if ReaderType.CASUAL.value in feedback:
            print(f"   Casual reader comments: {len(feedback[ReaderType.CASUAL.value])}")
            for i, comment in enumerate(feedback[ReaderType.CASUAL.value][:2], 1):
                print(f"   {i}. {comment}")
    except Exception as e:
        print(f"❌ Single reader feedback failed: {e}")
        return

    print("2. Testing multiple reader types feedback...")
    try:
        feedback_multi = await simulator.simulate_feedback(
            test_content,
            [ReaderType.CASUAL, ReaderType.CRITICAL, ReaderType.LORE]
        )
        print("✅ Multiple reader feedback generated")
        for reader_type, comments in feedback_multi.items():
            print(f"   {reader_type}: {len(comments)} comments")
            if comments:
                print(f"     Sample: {comments[0][:100]}...")
    except Exception as e:
        print(f"❌ Multiple reader feedback failed: {e}")

    print("✅ Feedback Simulator test completed!")

if __name__ == "__main__":
    asyncio.run(test_feedback_simulator())