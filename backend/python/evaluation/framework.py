"""Evaluation framework for intent recognition and response quality."""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class EvaluationMetrics:
    """Container for evaluation metrics."""
    intent_accuracy: float
    response_relevance: float
    response_accuracy: float
    response_completeness: float
    response_coherence: float
    overall_quality: float
    timestamp: datetime
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "intent_accuracy": self.intent_accuracy,
            "response_relevance": self.response_relevance,
            "response_accuracy": self.response_accuracy,
            "response_completeness": self.response_completeness,
            "response_coherence": self.response_coherence,
            "overall_quality": self.overall_quality,
            "timestamp": self.timestamp.isoformat()
        }


class EvaluationFramework:
    """Framework for evaluating agent performance."""
    
    def __init__(self, threshold: float = 0.95):
        """Initialize evaluation framework."""
        self.threshold = threshold
        self.metrics_history: List[EvaluationMetrics] = []
    
    def evaluate_interaction(
        self,
        query: str,
        intent: str,
        response: str,
        expected_intent: Optional[str] = None,
        expected_response: Optional[str] = None
    ) -> EvaluationMetrics:
        """Evaluate a single interaction."""
        from agents.evaluation_agent import EvaluationAgent
        
        eval_agent = EvaluationAgent()
        
        # Evaluate intent
        intent_eval = eval_agent.evaluate_intent(
            query=query,
            predicted_intent=intent,
            entities=[]
        )
        
        # Evaluate response
        response_eval = eval_agent.evaluate_response(
            query=query,
            response=response,
            context_used=True
        )
        
        # Calculate overall quality
        overall_quality = (
            intent_eval.get("overall_score", 0.5) +
            response_eval.get("overall_score", 0.5)
        ) / 2
        
        metrics = EvaluationMetrics(
            intent_accuracy=intent_eval.get("overall_score", 0.5),
            response_relevance=response_eval.get("relevance", 0.5),
            response_accuracy=response_eval.get("accuracy", 0.5),
            response_completeness=response_eval.get("completeness", 0.5),
            response_coherence=response_eval.get("coherence", 0.5),
            overall_quality=overall_quality,
            timestamp=datetime.now()
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_accuracy_stats(self) -> Dict[str, float]:
        """Get accuracy statistics from history."""
        if not self.metrics_history:
            return {
                "intent_accuracy": 0.0,
                "response_quality": 0.0,
                "overall_accuracy": 0.0,
                "total_evaluations": 0
            }
        
        intent_accuracies = [m.intent_accuracy for m in self.metrics_history]
        response_qualities = [m.overall_quality for m in self.metrics_history]
        overall_qualities = [m.overall_quality for m in self.metrics_history]
        
        return {
            "intent_accuracy": sum(intent_accuracies) / len(intent_accuracies),
            "response_quality": sum(response_qualities) / len(response_qualities),
            "overall_accuracy": sum(overall_qualities) / len(overall_qualities),
            "total_evaluations": len(self.metrics_history),
            "meets_threshold": (
                sum(overall_qualities) / len(overall_qualities) >= self.threshold
            )
        }
    
    def evaluate_batch(
        self,
        test_cases: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Evaluate a batch of test cases."""
        results = []
        
        for test_case in test_cases:
            metrics = self.evaluate_interaction(
                query=test_case["query"],
                intent=test_case.get("intent", "unknown"),
                response=test_case.get("response", ""),
                expected_intent=test_case.get("expected_intent"),
                expected_response=test_case.get("expected_response")
            )
            results.append(metrics.to_dict())
        
        stats = self.get_accuracy_stats()
        
        return {
            "results": results,
            "statistics": stats,
            "threshold": self.threshold,
            "meets_threshold": stats["overall_accuracy"] >= self.threshold
        }
    
    def export_metrics(self, filepath: str):
        """Export metrics to JSON file."""
        data = {
            "metrics": [m.to_dict() for m in self.metrics_history],
            "statistics": self.get_accuracy_stats(),
            "threshold": self.threshold
        }
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
    
    def clear_history(self):
        """Clear evaluation history."""
        self.metrics_history = []


# Global evaluation framework instance
evaluation_framework = EvaluationFramework(threshold=0.95)
