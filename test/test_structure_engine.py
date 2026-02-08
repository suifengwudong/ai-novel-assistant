#!/usr/bin/env python3
"""
Phase 4 结构化创作引擎测试脚本
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def test_basic_imports():
    """测试基本模块导入"""
    print("🧪 测试Phase 4结构化创作引擎基本功能...")

    try:
        # 只测试数据结构模块（不需要外部依赖）
        print("正在导入数据结构模块...")
        from backend.core.structure.models import (
            PlotNode, NovelProject, PlotLoop,
            NodeType, NodeStatus, PacingTemplate
        )
        print("✅ 数据结构模块导入成功")

        # 测试数据结构创建
        print("\n🏗️ 测试数据结构创建...")

        node = PlotNode(
            id="test_node_1",
            title="测试章节",
            description="这是一个测试章节的大纲",
            type=NodeType.CHAPTER
        )
        print(f"✅ PlotNode创建成功: {node.title} ({node.type.value})")

        project = NovelProject(
            id="test_project",
            title="测试小说项目",
            outline_tree=[node]
        )
        print(f"✅ NovelProject创建成功: {project.title}")

        loop = PlotLoop(
            id="test_loop_1",
            description="主角捡到的神秘戒指",
            created_in_node="test_node_1",
            importance="major"
        )
        print(f"✅ PlotLoop创建成功: {loop.description} ({loop.importance})")

        # 测试枚举
        print(f"✅ NodeType枚举: {NodeType.CHAPTER.value}")
        print(f"✅ NodeStatus枚举: {NodeStatus.DRAFT.value}")
        print(f"✅ PacingTemplate枚举: {PacingTemplate.HERO_JOURNEY.value}")

        # 测试项目方法
        open_loops = project.get_open_loops_count()
        print(f"✅ 项目方法测试: 未解决伏笔数 = {open_loops}")

        print("\n🎉 Phase 4结构化创作引擎基本功能测试通过！")
        print("\n📋 测试结果总结:")
        print("- ✅ 数据结构定义完整")
        print("- ✅ 类型安全 (使用枚举和数据类)")
        print("- ✅ 基础方法功能正常")
        print("- ✅ 可以进行小说项目建模")
        print("\n💡 提示: 其他模块(guardian, loop_tracker, pacer)需要LLM和数据库依赖，")
        print("         建议在完整环境中测试，或等待后端API集成后再进行全面测试。")

        return True

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("💡 提示: 请确保在项目根目录下运行，或检查Python路径")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_imports()
    sys.exit(0 if success else 1)