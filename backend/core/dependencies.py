"""
依赖注入容器
管理所有服务的生命周期和依赖关系
"""
from typing import Optional
from config.settings import settings
from core.llm.litellm_client import LiteLLMClient
from database.vector_store import VectorStore
from database.db_client import DatabaseClient
from core.memory.knowledge_graph import KnowledgeGraph
from core.structure.guardian import OutlineGuardian
from core.validation.logic_validator import LogicValidator
from loguru import logger

class DependencyContainer:
    """
    依赖注入容器
    单例模式，确保服务实例的唯一性和生命周期管理
    """

    _instance: Optional['DependencyContainer'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._llm_client: Optional[LiteLLMClient] = None
            self._vector_store: Optional[VectorStore] = None
            self._knowledge_graph: Optional[KnowledgeGraph] = None
            self._outline_guardian: Optional[OutlineGuardian] = None
            self._logic_validator: Optional[LogicValidator] = None
            self._db_client: Optional[DatabaseClient] = None

    @property
    def llm_client(self) -> LiteLLMClient:
        if self._llm_client is None:
            self._llm_client = LiteLLMClient()
        return self._llm_client

    @property
    def vector_store(self) -> VectorStore:
        if self._vector_store is None:
            try:
                self._vector_store = VectorStore(
                    collection_name="novel_knowledge",
                    persist_directory=settings.vector_store_path
                )
            except Exception as e:
                logger.error(f"Failed to initialize VectorStore: {e}")
                raise
        return self._vector_store

    @property
    def db_client(self) -> DatabaseClient:
        if self._db_client is None:
            try:
                self._db_client = DatabaseClient(settings.database_url)
            except Exception as e:
                logger.error(f"Failed to initialize DatabaseClient: {e}")
                raise
        return self._db_client

    @property
    def knowledge_graph(self) -> KnowledgeGraph:
        if self._knowledge_graph is None:
            self._knowledge_graph = KnowledgeGraph(self.db_client)
        return self._knowledge_graph

    @property
    def outline_guardian(self) -> OutlineGuardian:
        if self._outline_guardian is None:
            self._outline_guardian = OutlineGuardian(self.llm_client)
        return self._outline_guardian

    @property
    def logic_validator(self) -> LogicValidator:
        if self._logic_validator is None:
            self._logic_validator = LogicValidator(self.llm_client)
        return self._logic_validator

# 全局容器实例
container = DependencyContainer()