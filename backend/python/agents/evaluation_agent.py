"""Evaluation agent for monitoring response quality."""
from typing import Dict, Optional, Any
from agents.base_agent import BaseAgent
import json


class EvaluationAgent(BaseAgent):
    """Agent responsible for evaluating response quality and intent recognition."""
    
    def __init__(self):
        system_prompt = """You are an Evaluation Agent specialized in assessing the quality of AI responses and intent recognition.

Your responsibilities:
1. Evaluate intent recognition accuracy
2. Assess response relevance to the query
3. Check response quality (coherence, completeness, accuracy)
4. Provide scores and feedback for improvement

Evaluate on a scale of 0-1 for each metric."""
        super().__init__(
            name="EvaluationAgent",
            system_prompt=system_prompt,
            temperature=0.1  # Very low temperature for consistent evaluation
        )
    
    def evaluate_intent(
        self,
        query: str,
        predicted_intent: str,
        entities: list
    ) -> Dict[str, Any]:
        """Evaluate intent recognition accuracy."""
        prompt = f"""Query: {query}
Predicted Intent: {predicted_intent}
Extracted Entities: {entities}

Evaluate the intent recognition:
1. Is the predicted intent correct? (0-1)
2. Are the entities relevant? (0-1)
3. Overall intent recognition score (0-1)

Respond with JSON: {{"intent_correct": 0.0-1.0, "entities_relevant": 0.0-1.0, "overall_score": 0.0-1.0}}"""
        
        messages = self._build_messages(prompt)
        
        try:
            response = self._invoke_llm(messages)
            content = response.content
            
            # Extract JSON
            if "{" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                content = content[json_start:json_end]
            
            evaluation = json.loads(content)
            return {
                "intent_correct": evaluation.get("intent_correct", 0.5),
                "entities_relevant": evaluation.get("entities_relevant", 0.5),
                "overall_score": evaluation.get("overall_score", 0.5)
            }
        except Exception as e:
            return {
                "intent_correct": 0.5,
                "entities_relevant": 0.5,
                "overall_score": 0.5,
                "error": str(e)
            }
    
    def evaluate_response(
        self,
        query: str,
        response: str,
        context_used: bool = False
    ) -> Dict[str, Any]:
        """Evaluate response quality."""
        prompt = f"""Query: {query}
Response: {response}
Context Used: {context_used}

Evaluate the response quality:
1. Relevance: How relevant is the response to the query? (0-1)
2. Accuracy: Is the information accurate? (0-1)
3. Completeness: Does it fully address the query? (0-1)
4. Coherence: Is it well-structured and coherent? (0-1)
5. Overall quality score (0-1)

Respond with JSON: {{"relevance": 0.0-1.0, "accuracy": 0.0-1.0, "completeness": 0.0-1.0, "coherence": 0.0-1.0, "overall_score": 0.0-1.0}}"""
        
        messages = self._build_messages(prompt)
        
        try:
            response_obj = self._invoke_llm(messages)
            content = response_obj.content
            
            # Extract JSON
            if "{" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                content = content[json_start:json_end]
            
            evaluation = json.loads(content)
            return {
                "relevance": evaluation.get("relevance", 0.5),
                "accuracy": evaluation.get("accuracy", 0.5),
                "completeness": evaluation.get("completeness", 0.5),
                "coherence": evaluation.get("coherence", 0.5),
                "overall_score": evaluation.get("overall_score", 0.5)
            }
        except Exception as e:
            return {
                "relevance": 0.5,
                "accuracy": 0.5,
                "completeness": 0.5,
                "coherence": 0.5,
                "overall_score": 0.5,
                "error": str(e)
            }
    
    def process(self, user_input: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Evaluate the entire interaction."""
        if not context:
            return {"error": "No context provided for evaluation"}
        
        intent_eval = None
        response_eval = None
        
        # Evaluate intent if available
        if "intent" in context:
            intent_eval = self.evaluate_intent(
                query=context.get("original_query", user_input),
                predicted_intent=context.get("intent"),
                entities=context.get("entities", [])
            )
        
        # Evaluate response if available
        if "response" in context:
            response_eval = self.evaluate_response(
                query=context.get("original_query", user_input),
                response=context.get("response"),
                context_used=context.get("used_context", False)
            )
        
        return {
            "agent": self.name,
            "intent_evaluation": intent_eval,
            "response_evaluation": response_eval,
            "overall_quality": (
                (intent_eval.get("overall_score", 0.5) + response_eval.get("overall_score", 0.5)) / 2
                if intent_eval and response_eval
                else 0.5
            )
        }
