"""ChromaDB vector store integration for RAG."""
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from langchain_core.documents import Document
from config.settings import settings

import chromadb
from chromadb.config import Settings as ChromaSettings


class PortfolioVectorStore:
    """ChromaDB vector store wrapper for portfolio knowledge base."""

    def __init__(self):
        """Initialize ChromaDB with persistent local storage."""
        persist_dir = str(Path(__file__).resolve().parents[3] / "data" / "chroma_db")
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"ChromaDB initialized at {persist_dir} (collection: {settings.CHROMA_COLLECTION_NAME}, docs: {self.collection.count()})")

    def add_documents(self, documents: List[Document], batch_size: int = 100):
        """Add documents to ChromaDB."""
        if not documents:
            return
        ids = [f"doc_{i}_{hash(d.page_content) % 100000}" for i, d in enumerate(documents)]
        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]

        for i in range(0, len(texts), batch_size):
            self.collection.upsert(
                ids=ids[i:i + batch_size],
                documents=texts[i:i + batch_size],
                metadatas=metadatas[i:i + batch_size]
            )
        print(f"Added {len(documents)} documents to ChromaDB")

    def similarity_search(
        self,
        query: str,
        k: int = None,
        filter: Optional[Dict] = None
    ) -> List[Document]:
        """Perform similarity search."""
        k = k or settings.TOP_K_RESULTS
        kwargs = {"query_texts": [query], "n_results": min(k, self.collection.count() or 1)}
        if filter:
            kwargs["where"] = filter
        try:
            results = self.collection.query(**kwargs)
            documents = []
            for i, doc_text in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                documents.append(Document(page_content=doc_text, metadata=metadata))
            return documents
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return []

    def similarity_search_with_score(
        self,
        query: str,
        k: int = None,
        filter: Optional[Dict] = None
    ) -> List[Tuple[Document, float]]:
        """Perform similarity search with relevance scores."""
        k = k or settings.TOP_K_RESULTS
        kwargs = {
            "query_texts": [query],
            "n_results": min(k, self.collection.count() or 1),
            "include": ["documents", "metadatas", "distances"]
        }
        if filter:
            kwargs["where"] = filter
        try:
            results = self.collection.query(**kwargs)
            scored_docs = []
            for i, doc_text in enumerate(results["documents"][0]):
                metadata = results["metadatas"][0][i] if results["metadatas"] else {}
                distance = results["distances"][0][i] if results["distances"] else 0
                score = 1 - distance  # cosine distance -> similarity
                scored_docs.append((Document(page_content=doc_text, metadata=metadata), score))
            return scored_docs
        except Exception as e:
            print(f"Error in similarity search with score: {e}")
            return []

    def delete_all(self):
        """Delete all documents from the collection."""
        self.client.delete_collection(settings.CHROMA_COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print("Deleted all documents from ChromaDB")

    def get_stats(self) -> Dict:
        """Get collection statistics."""
        count = self.collection.count()
        return {
            "total_vectors": count,
            "collection": settings.CHROMA_COLLECTION_NAME,
            "backend": "ChromaDB (local)"
        }


vector_store = PortfolioVectorStore()
