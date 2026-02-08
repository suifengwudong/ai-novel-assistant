"""
测试风格学习系统
"""
import sys
import os
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.style_learning import StyleLearner, StyleProfile
from core.llm.litellm_client import LiteLLMClient

async def test_style_learning():
    print("Testing Style Learning System...")

    # Mock DB client
    class MockDB:
        def __init__(self):
            self.styles = {}

        async def save_style(self, style_data):
            self.styles[style_data['id']] = style_data

        async def get_style(self, style_id):
            return self.styles.get(style_id)

    llm_client = LiteLLMClient()
    db = MockDB()
    learner = StyleLearner(llm_client, db)

    # Test style analysis
    sample_text = """
    夕阳西下，古老的城堡矗立在山巅。风中传来阵阵狼啸，艾丽丝紧握手中的古剑。
    她的心跳如战鼓般急促，却又带着一丝莫名的兴奋。

    "这把剑承载了太多的秘密，"她喃喃自语，"但我必须前行。"

    森林的阴影在暮色中拉长，未知的危险在前方等待。但艾丽丝的眼中燃烧着不屈的火焰。
    """

    print("1. Testing style analysis...")
    try:
        profile = await learner.analyze_style(sample_text, "奇幻冒险风格")
        print(f"✅ Style analysis completed: {profile.name}")
        print(f"   - Tone: {profile.tone}")
        print(f"   - Lexical features: {len(profile.lexical_features)}")
        print(f"   - Sentence patterns: {len(profile.sentence_patterns)}")
        print(f"   - Rhetorical devices: {len(profile.rhetorical_devices)}")
    except Exception as e:
        print(f"❌ Style analysis failed: {e}")
        return

    # Test style prompt generation
    print("2. Testing style prompt generation...")
    try:
        prompt = learner.get_style_prompt(profile)
        print("✅ Style prompt generated successfully")
        print(f"Prompt preview: {prompt[:200]}...")
    except Exception as e:
        print(f"❌ Style prompt generation failed: {e}")

    print("✅ Style Learning System test completed!")

if __name__ == "__main__":
    asyncio.run(test_style_learning())