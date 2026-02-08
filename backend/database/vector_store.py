"""
向量数据库适配器
实现基于语义的文本检索
"""
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.utils import embedding_functions
from loguru import logger

class VectorStore:
    def __init__(self, collection_name: str = "novel_knowledge", persist_directory: str = "./data/chroma"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # 使用默认的 sentence-transformers 嵌入模型
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )
        logger.info(f"VectorStore initialized with collection: {collection_name}")

    async def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """添加文本向量"""
        try:
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(texts)} documents to vector store")
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise

    async def search(self, query: str, top_k: int = 5, filter: Optional[Dict] = None) -> List[Dict]:
        """语义搜索"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filter
            )
            
            # 格式化返回结果
            formatted_results = []
            if results["documents"]:
                for i, doc in enumerate(results["documents"][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "score": results["distances"][0][i] if results["distances"] else 0
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []

    async def delete(self, ids: List[str]):
        """删除向量"""
        self.collection.delete(ids=ids)