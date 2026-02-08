"""
数据库客户端
提供统一的数据库访问接口
"""
from typing import Any, List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger

class DatabaseClient:
    """
    数据库客户端
    封装SQLAlchemy，提供统一的数据库操作接口
    """

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info(f"Database client initialized with URL: {database_url}")

    def get_session(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()

    def execute(self, query: str, params: Optional[List[Any]] = None):
        """执行SQL查询"""
        with self.get_session() as session:
            try:
                if params:
                    result = session.execute(text(query), params)
                else:
                    result = session.execute(text(query))
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                logger.error(f"Database execute error: {e}")
                raise

    def fetchall(self, query: str, params: Optional[List[Any]] = None) -> List[tuple]:
        """查询多行数据"""
        with self.get_session() as session:
            try:
                if params:
                    result = session.execute(text(query), params)
                else:
                    result = session.execute(text(query))
                return result.fetchall()
            except Exception as e:
                logger.error(f"Database fetchall error: {e}")
                raise

    def fetchone(self, query: str, params: Optional[List[Any]] = None) -> Optional[tuple]:
        """查询单行数据"""
        with self.get_session() as session:
            try:
                if params:
                    result = session.execute(text(query), params)
                else:
                    result = session.execute(text(query))
                return result.fetchone()
            except Exception as e:
                logger.error(f"Database fetchone error: {e}")
                raise