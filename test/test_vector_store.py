"""
测试向量存储模块
"""
import sys
import os
import asyncio
import tempfile
import shutil

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database.vector_store import VectorStore

async def test_vector_store():
    print("Testing VectorStore...")

    # Create temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    try:
        # Initialize vector store
        store = VectorStore(collection_name="test_collection", persist_directory=temp_dir)

        # Test adding texts
        texts = [
            "Alice is a brave adventurer who loves exploring ancient ruins.",
            "Bob is Alice's loyal companion, a skilled archer.",
            "The ancient sword grants magical powers to its wielder."
        ]
        metadatas = [
            {"type": "character", "name": "Alice"},
            {"type": "character", "name": "Bob"},
            {"type": "item", "name": "sword"}
        ]
        ids = ["alice_desc", "bob_desc", "sword_desc"]

        await store.add_texts(texts, metadatas, ids)
        print("✅ Added texts successfully")

        # Test searching
        results = await store.search("brave adventurer", top_k=2)
        print(f"Search results: {len(results)} found")
        for result in results:
            print(f"  - {result['content'][:50]}... (score: {result['score']:.3f})")

        # Test filtered search
        filtered_results = await store.search("sword", filter={"type": "item"})
        print(f"Filtered search results: {len(filtered_results)} found")

        print("✅ VectorStore tests passed!")

    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    asyncio.run(test_vector_store())
