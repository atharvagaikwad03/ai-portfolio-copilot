"""Query agent for intent recognition and query processing."""
from typing import Dict, Optional, Any
from agents.base_agent import BaseAgent
import json


class QueryAgent(BaseAgent):
    """Agent responsible for understanding user queries and intent."""
    
    def __init__(self):
        system_prompt = """You are a Query Agent specialized in understanding user intent and processing queries.
        
Your responsibilities:
1. Analyze user queries to identify intent (information request, question, conversation, etc.)
2. Extract key entities and topics from queries
3. Determine if the query requires retrieval from knowledge base
4. Classify query type (factual, conversational, project-related, etc.)

Respond with a JSON object containing:
- intent: The identified intent
- entities: List of key entities/topics
- requires_retrieval: Boolean indicating if RAG retrieval is needed
- query_type: Type of query
- confidence: Confidence score (0-1)
"""
        super().__init__(
            name="QueryAgent",
            system_prompt=system_prompt,
            temperature=0.3  # Lower temperature for more consistent intent recognition
        )
    
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process query and extract intent."""
        messages = self._build_messages(
            f"Analyze this user query: {user_input}\n\nProvide your analysis as JSON."
        )
        
        try:
            response = self._invoke_llm(messages)
            content = response.content
            
            # Try to extract JSON from response
            if "```json" in content:
                json_start = content.find("```json") + 7
                json_end = content.find("```", json_start)
                content = content[json_start:json_end].strip()
            elif "{" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                content = content[json_start:json_end]
            
            analysis = json.loads(content)
            
            return {
                "agent": self.name,
                "intent": analysis.get("intent", "unknown"),
                "entities": analysis.get("entities", []),
                "requires_retrieval": analysis.get("requires_retrieval", True),
                "query_type": analysis.get("query_type", "general"),
                "confidence": analysis.get("confidence", 0.8),
                "original_query": user_input
            }
        except Exception as e:
            # Fallback response
            return {
                "agent": self.name,
                "intent": "information_request",
                "entities": [],
                "requires_retrieval": True,
                "query_type": "general",
                "confidence": 0.5,
                "original_query": user_input,
                "error": str(e)
            }
