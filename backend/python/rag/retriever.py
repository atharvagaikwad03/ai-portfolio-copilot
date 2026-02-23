"""RAG retriever with query processing and context retrieval."""
from typing import List, Dict, Optional
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.vector_store import vector_store
from config.settings import settings
import time


class RAGRetriever:
    """Retrieval component for RAG architecture."""
    
    def __init__(self):
        """Initialize RAG retriever."""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        self.vector_store = vector_store
    
    def process_and_store_documents(
        self,
        documents: List[Document],
        metadata: Optional[Dict] = None
    ):
        """Process documents and store in vector database."""
        # Add metadata if provided
        if metadata:
            for doc in documents:
                doc.metadata.update(metadata)
        
        # Split documents into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Store in vector database
        self.vector_store.add_documents(chunks)
        
        return len(chunks)
    
    def retrieve_context(
        self,
        query: str,
        k: int = None,
        score_threshold: float = 0.7,
        metadata_filter: Optional[Dict] = None
    ) -> List[Document]:
        """Retrieve relevant context for a query."""
        start_time = time.time()
        
        # Perform similarity search
        if metadata_filter:
            results = self.vector_store.similarity_search(
                query=query,
                k=k or settings.TOP_K_RESULTS,
                filter=metadata_filter
            )
        else:
            results = self.vector_store.similarity_search(
                query=query,
                k=k or settings.TOP_K_RESULTS
            )
        
        # Filter by score threshold if using scored search
        if score_threshold > 0:
            scored_results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k or settings.TOP_K_RESULTS,
                filter=metadata_filter
            )
            results = [
                doc for doc, score in scored_results
                if score >= score_threshold
            ]
        
        retrieval_time = time.time() - start_time
        
        return {
            "documents": results,
            "retrieval_time": retrieval_time,
            "num_results": len(results)
        }
    
    def format_context(self, documents: List[Document]) -> str:
        """Format retrieved documents into context string."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            content = doc.page_content
            metadata = doc.metadata
            source = metadata.get("source", "Unknown")
            context_parts.append(f"[{i}] Source: {source}\n{content}\n")
        
        return "\n".join(context_parts)
    
    def hybrid_search(
        self,
        query: str,
        k: int = None,
        keyword_weight: float = 0.3
    ) -> List[Document]:
        """Hybrid search combining semantic and keyword search."""
        # Semantic search
        semantic_results = self.retrieve_context(query, k=k * 2)
        
        # Keyword search (simple implementation)
        query_keywords = set(query.lower().split())
        
        # Re-rank results based on keyword matches
        scored_results = []
        for doc in semantic_results["documents"]:
            doc_keywords = set(doc.page_content.lower().split())
            keyword_overlap = len(query_keywords & doc_keywords) / len(query_keywords) if query_keywords else 0
            
            # Combine semantic and keyword scores
            # In production, use a proper re-ranking model
            score = (1 - keyword_weight) + (keyword_weight * keyword_overlap)
            scored_results.append((doc, score))
        
        # Sort by combined score
        scored_results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k
        return [doc for doc, _ in scored_results[:k or settings.TOP_K_RESULTS]]


# Global retriever instance
retriever = RAGRetriever()
