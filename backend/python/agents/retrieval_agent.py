"""Retrieval agent for RAG operations."""
from typing import Dict, Optional, Any
from agents.base_agent import BaseAgent
from rag.retriever import retriever


class RetrievalAgent(BaseAgent):
    """Agent responsible for retrieving relevant context from knowledge base."""
    
    def __init__(self):
        system_prompt = """You are a Retrieval Agent specialized in finding relevant information from a knowledge base.

Your responsibilities:
1. Understand what information is needed based on the query
2. Retrieve relevant context from the vector database
3. Rank and filter retrieved documents by relevance
4. Format retrieved context for use by other agents

Focus on retrieving the most relevant and useful information."""
        super().__init__(
            name="RetrievalAgent",
            system_prompt=system_prompt,
            temperature=0.2
        )
        self.retriever = retriever
    
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Retrieve relevant context for the query."""
        query = context.get("original_query", user_input) if context else user_input
        
        # Retrieve context
        retrieval_result = self.retriever.retrieve_context(
            query=query,
            k=context.get("top_k", 5) if context else 5,
            score_threshold=0.7
        )
        
        # Format context
        formatted_context = self.retriever.format_context(
            retrieval_result["documents"]
        )
        
        return {
            "agent": self.name,
            "query": query,
            "documents": retrieval_result["documents"],
            "formatted_context": formatted_context,
            "retrieval_time": retrieval_result["retrieval_time"],
            "num_results": retrieval_result["num_results"],
            "success": retrieval_result["num_results"] > 0
        }
