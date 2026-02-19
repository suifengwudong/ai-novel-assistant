"""
测试API路由挂载 (Phase 3 Step 1)
验证后端API路由是否正确注册
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

def test_api_routes():
    """测试API路由是否正确挂载"""
    print("🧪 测试API路由挂载...")

    import main  # noqa: F401 – triggers app init

    # Collect all registered routes
    routes = {
        route.path: list(route.methods)
        for route in main.app.routes
        if hasattr(route, 'methods') and route.methods
    }

    print("已注册路由:")
    for path, methods in routes.items():
        print(f"  {methods} {path}")

    # Assert the three endpoints the frontend depends on
    required = [
        ("/api/v1/style/analyze", "POST"),
        ("/api/v1/agent/polish", "POST"),
        ("/api/v1/agent/feedback", "POST"),
        ("/api/v1/agent/generate/stream", "POST"),
    ]

    all_ok = True
    for path, method in required:
        if path in routes and method in routes[path]:
            print(f"✅ {method} {path}")
        else:
            print(f"❌ {method} {path} — 未找到!")
            all_ok = False

    if all_ok:
        print("\n🎉 所有必要路由已正确挂载！")
    else:
        print("\n❌ 部分路由缺失，请检查 main.py 和 api/routes/")
    return all_ok


def test_settings_fields():
    """测试settings字段名称是否与main.py期望一致"""
    print("\n🧪 测试Settings字段...")

    from config.settings import settings

    required_fields = ["ENVIRONMENT", "LLM_PROVIDER", "CORS_ORIGINS", "API_PORT", "LOG_LEVEL"]
    all_ok = True
    for field in required_fields:
        val = getattr(settings, field, None)
        if val is not None:
            print(f"✅ settings.{field} = {val}")
        else:
            print(f"❌ settings.{field} — 字段不存在!")
            all_ok = False

    return all_ok


def test_litellm_client_importable():
    """测试LiteLLMClient可以被导入"""
    print("\n🧪 测试LiteLLMClient导入...")
    try:
        from core.llm.litellm_client import LiteLLMClient
        client = LiteLLMClient()
        assert hasattr(client, 'generate'), "缺少 generate 方法"
        assert hasattr(client, 'generate_stream'), "缺少 generate_stream 方法"
        print(f"✅ LiteLLMClient 导入成功，model={client.model}")
        return True
    except Exception as e:
        print(f"❌ LiteLLMClient 导入失败: {e}")
        return False


if __name__ == "__main__":
    results = [
        test_settings_fields(),
        test_litellm_client_importable(),
        test_api_routes(),
    ]
    success = all(results)
    print("\n" + ("✅ 全部测试通过！" if success else "❌ 存在测试失败！"))
    sys.exit(0 if success else 1)
