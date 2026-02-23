"""Multi-agent orchestrator for coordinating agent workflows."""
from typing import Dict, Optional, Any, List
from agents.query_agent import QueryAgent
from agents.retrieval_agent import RetrievalAgent
from agents.response_agent import ResponseAgent
from agents.evaluation_agent import EvaluationAgent
from config.settings import settings
import time


class AgentOrchestrator:
    """Orchestrates multi-agent collaboration workflows."""
    
    def __init__(self):
        """Initialize orchestrator with all agents."""
        self.query_agent = QueryAgent()
        self.retrieval_agent = RetrievalAgent()
        self.response_agent = ResponseAgent()
        self.evaluation_agent = EvaluationAgent()
        self.agents = {
            "query": self.query_agent,
            "retrieval": self.retrieval_agent,
            "response": self.response_agent,
            "evaluation": self.evaluation_agent
        }
    
    def process_query(
        self,
        user_input: str,
        session_id: Optional[str] = None,
        enable_evaluation: bool = None
    ) -> Dict[str, Any]:
        """Process a user query through the multi-agent pipeline."""
        start_time = time.time()
        enable_evaluation = enable_evaluation if enable_evaluation is not None else settings.EVAL_MODE
        
        # Step 1: Query Agent - Intent Recognition
        query_result = self.query_agent.process(user_input)
        
        # Step 2: Retrieval Agent - RAG (if needed)
        retrieval_result = None
        if query_result.get("requires_retrieval", True):
            retrieval_result = self.retrieval_agent.process(
                user_input,
                context=query_result
            )
        
        # Step 3: Response Agent - Generate Response
        response_context = {
            **query_result,
            "formatted_context": retrieval_result.get("formatted_context") if retrieval_result else None
        }
        response_result = self.response_agent.process(
            user_input,
            context=response_context
        )
        
        # Step 4: Evaluation Agent - Quality Check (if enabled)
        evaluation_result = None
        should_evaluate = (
            enable_evaluation
            and "error" not in query_result
            and not response_result.get("fallback_used", False)
            and response_result.get("success", True)
        )
        if should_evaluate:
            eval_context = {
                **query_result,
                "response": response_result.get("response"),
                "used_context": response_result.get("used_context", False)
            }
            evaluation_result = self.evaluation_agent.process(
                user_input,
                context=eval_context
            )
        
        total_time = time.time() - start_time
        
        # Compile final result
        result = {
            "session_id": session_id,
            "query": user_input,
            "response": response_result.get("response"),
            "intent": query_result.get("intent"),
            "entities": query_result.get("entities", []),
            "query_type": query_result.get("query_type"),
            "confidence": query_result.get("confidence"),
            "retrieval_used": retrieval_result is not None,
            "retrieval_time": retrieval_result.get("retrieval_time") if retrieval_result else None,
            "num_retrieved_docs": retrieval_result.get("num_results") if retrieval_result else 0,
            "total_time": total_time,
            "agents_used": ["query", "retrieval", "response"] + (["evaluation"] if should_evaluate else [])
        }
        
        # Add evaluation metrics if available
        if evaluation_result:
            result["evaluation"] = {
                "intent_accuracy": evaluation_result.get("intent_evaluation", {}).get("overall_score"),
                "response_quality": evaluation_result.get("response_evaluation", {}).get("overall_score"),
                "overall_quality": evaluation_result.get("overall_quality")
            }
        
        return result
    
    def tool_calling_workflow(
        self,
        user_input: str,
        tools: List,
        max_iterations: int = None
    ) -> Dict[str, Any]:
        """Execute a tool-calling workflow."""
        max_iterations = max_iterations or settings.MAX_TOOL_CALLS
        
        # Use query agent to determine which tools to use
        query_result = self.query_agent.process(user_input)
        
        # Simple tool selection based on entities
        selected_tools = []
        entities = query_result.get("entities", [])
        
        # Tool selection logic (simplified)
        for tool in tools:
            if any(entity.lower() in tool.name.lower() for entity in entities):
                selected_tools.append(tool)
        
        # Execute tools
        tool_results = []
        for tool in selected_tools[:max_iterations]:
            try:
                result = tool.run(user_input)
                tool_results.append({
                    "tool": tool.name,
                    "result": result
                })
            except Exception as e:
                tool_results.append({
                    "tool": tool.name,
                    "error": str(e)
                })
        
        # Generate response using tool results
        context = {
            **query_result,
            "tool_results": tool_results
        }
        response_result = self.response_agent.process(user_input, context=context)
        
        return {
            "query": user_input,
            "response": response_result.get("response"),
            "tools_used": [r["tool"] for r in tool_results],
            "tool_results": tool_results
        }
    
    def get_agent_stats(self) -> Dict[str, Any]:
        """Get statistics about agent usage."""
        return {
            "agents": list(self.agents.keys()),
            "query_agent_history_length": len(self.query_agent.conversation_history),
            "response_agent_history_length": len(self.response_agent.conversation_history)
        }
    
    def clear_all_histories(self):
        """Clear conversation histories for all agents."""
        for agent in self.agents.values():
            agent.clear_history()


# Global orchestrator instance
orchestrator = AgentOrchestrator()
