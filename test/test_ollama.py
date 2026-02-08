import sys
import os
import asyncio

# Add the 'backend' directory to sys.path so imports like 'config.settings' work
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, "..", "backend")
sys.path.insert(0, backend_dir)

# Now we can import as if we are inside 'backend/'
from config.settings import settings
from core.llm.litellm_client import LiteLLMClient

async def test_ollama():
    print("Loading settings...")
    try:
        # Settings are singletons loaded on import usually, but we check values here
        print(f"Provider: {settings.provider}")
        print(f"Model: {settings.model}")
        print(f"Base URL: {settings.base_url}")
    except Exception as e:
        print(f"Error loading settings: {e}")
        return

    print("\nInitializing LiteLLM Client...")
    try:
        client = LiteLLMClient() # No args, uses imported settings
    except Exception as e:
        print(f"Error initializing client: {e}")
        return

        print(f"\nTesting connection to {settings.model} via {settings.provider}...")
    prompt = "Hello! Are you working? Please reply with 'Yes, I am working!'."
    
    try:
        # Check method signature of generate. Assuming it returns response string or object
        response = await client.generate(
            prompt=prompt,
            system_message="You are a helpful assistant."
        )
        print("\nResponse received:")
        print("-" * 20)
        print(response)
        print("-" * 20)
        print("\n✅ Debugging Successful!")
    except Exception as e:
        print("\n❌ Error during generation:")
        print(e)
        print("\nTips:")
        print("1. Make sure Ollama is running (check task manager or run 'ollama serve').")
        print(f"2. Make sure the model '{settings.LLM_MODEL}' is pulled (run 'ollama pull {settings.LLM_MODEL}').")

if __name__ == "__main__":
    asyncio.run(test_ollama())
