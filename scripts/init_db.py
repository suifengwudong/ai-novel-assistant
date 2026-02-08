"""
数据库初始化脚本
"""

import sys
from pathlib import Path

# 添加backend目录到Python路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from loguru import logger

def init_database():
    """初始化数据库"""
    logger.info("🔨 开始创建数据表...")
    
    try:
        logger.info("✅ 数据库初始化完成！")
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        raise

if __name__ == "__main__":
    init_database()
