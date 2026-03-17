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

    def _fallback_analysis(self, user_input: str) -> Dict[str, Any]:
        """Classify common portfolio questions without the LLM."""
        query = user_input.lower()

        if any(token in query for token in ["hello", "hi", "hey", "good morning", "good evening"]):
            intent = "greeting"
            query_type = "conversational"
        elif any(token in query for token in ["who are you", "who is atharva", "tell me about yourself", "tell me about atharva"]):
            intent = "profile_summary"
            query_type = "general"
        elif any(token in query for token in ["project", "free flow", "portfolio copilot", "built"]):
            intent = "project_inquiry"
            query_type = "project-related"
        elif any(token in query for token in ["skill", "tech", "stack", "language", "framework"]):
            intent = "skills_inquiry"
            query_type = "factual"
        elif any(token in query for token in ["experience", "work", "company", "intern", "job"]):
            intent = "experience_inquiry"
            query_type = "factual"
        elif any(token in query for token in ["education", "degree", "university", "gpa", "study"]):
            intent = "education_inquiry"
            query_type = "factual"
        elif any(token in query for token in ["contact", "email", "linkedin", "github", "reach"]):
            intent = "contact_inquiry"
            query_type = "factual"
        else:
            intent = "information_request"
            query_type = "general"

        entities = []
        for token in ["free flow", "ai portfolio copilot", "react", "python", "cerence ai", "syracuse university"]:
            if token in query:
                entities.append(token)

        return {
            "agent": self.name,
            "intent": intent,
            "entities": entities,
            "requires_retrieval": False,
            "query_type": query_type,
            "confidence": 0.75,
            "original_query": user_input,
        }

    def _should_use_local_classification(self, user_input: str) -> bool:
        """Short-circuit obvious portfolio questions to avoid unnecessary LLM calls."""
        query = user_input.lower()
        local_tokens = [
            "hello", "hi", "hey", "good morning", "good evening",
            "who are you", "who is atharva", "tell me about yourself", "tell me about atharva",
            "project", "free flow", "portfolio copilot", "built",
            "skill", "tech", "stack", "language", "framework",
            "experience", "work", "company", "intern", "job",
            "education", "degree", "university", "gpa", "study",
            "contact", "email", "linkedin", "github", "reach",
        ]
        return any(token in query for token in local_tokens)
    
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Process query and extract intent."""
        if self._should_use_local_classification(user_input):
            return self._fallback_analysis(user_input)

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
            fallback = self._fallback_analysis(user_input)
            fallback["error"] = str(e)
            return fallback
