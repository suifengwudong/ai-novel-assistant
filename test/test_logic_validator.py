"""
测试逻辑校验器
"""
import sys
import os
import asyncio

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from core.validation.logic_validator import LogicValidator
from core.llm.litellm_client import LiteLLMClient

async def test_logic_validator():
    print("Testing LogicValidator...")

    # Initialize LLM client (assuming Ollama is configured)
    llm_client = LiteLLMClient()

    # Initialize validator
    validator = LogicValidator(llm_client)

    # Test content
    content = "Alice picked up the ancient sword and became invisible. She then used her new power to sneak past the guards."

    # Core knowledge
    core_knowledge = [
        "Alice is a human adventurer with no magical abilities.",
        "The ancient sword grants invisibility to magical beings only.",
        "Alice cannot become invisible as she is not magical."
    ]

    # Locked settings
    locked_settings = {
        "world_rules": "Only magical creatures can use magic items",
        "character_constraints": "Alice remains human throughout the story"
    }

    # Run validation
    result = await validator.check(content, core_knowledge, locked_settings)

    print("Validation result:")
    print(f"  Passed: {result.get('passed', 'N/A')}")
    print(f"  Issues: {result.get('issues', [])}")
    print(f"  Suggestions: {result.get('suggestions', [])}")

    print("✅ LogicValidator test completed!")

if __name__ == "__main__":
    asyncio.run(test_logic_validator())
