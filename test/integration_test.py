"""
前后端集成测试脚本
"""
import requests
import time

def test_integration():
    print("🔗 测试前后端集成...")

    # 测试后端直接访问
    try:
        response = requests.get("http://localhost:8004/health")
        if response.status_code == 200:
            print("✅ 后端API直接访问正常")
            print(f"   响应: {response.json()}")
        else:
            print(f"❌ 后端API直接访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 后端连接失败: {e}")
        return False

    # 测试前端代理
    try:
        # 通过前端代理访问后端
        response = requests.get("http://localhost:3000/api/health")
        if response.status_code == 200:
            print("✅ 前端代理访问正常")
            print(f"   响应: {response.json()}")
        else:
            print(f"⚠️ 前端代理访问状态码: {response.status_code}")
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 前端代理访问失败: {e}")

    # 测试API文档
    try:
        response = requests.get("http://localhost:8004/docs")
        if response.status_code == 200:
            print("✅ API文档可访问")
        else:
            print(f"⚠️ API文档访问状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ API文档访问失败: {e}")

    print("\n🎉 集成测试完成！")
    print("📱 前端界面: http://localhost:3000")
    print("🔗 后端API: http://localhost:8004")
    print("📚 API文档: http://localhost:8004/docs")

    return True

if __name__ == "__main__":
    test_integration()