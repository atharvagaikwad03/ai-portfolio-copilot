"""Tests for agent system."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "backend" / "python"))

from agents.query_agent import QueryAgent
from agents.response_agent import ResponseAgent
from agents.orchestrator import AgentOrchestrator


@pytest.fixture
def query_agent():
    """Create a query agent instance."""
    return QueryAgent()


@pytest.fixture
def response_agent():
    """Create a response agent instance."""
    return ResponseAgent()


@pytest.fixture
def orchestrator():
    """Create an orchestrator instance."""
    return AgentOrchestrator()


def test_query_agent_intent_recognition(query_agent):
    """Test query agent intent recognition."""
    result = query_agent.process("Tell me about your projects")
    
    assert "intent" in result
    assert "entities" in result
    assert "requires_retrieval" in result
    assert "confidence" in result
    assert result["confidence"] >= 0.0
    assert result["confidence"] <= 1.0


def test_response_agent_generation(response_agent):
    """Test response agent response generation."""
    result = response_agent.process("Hello")
    
    assert "response" in result
    assert "success" in result
    assert len(result["response"]) > 0


def test_orchestrator_full_pipeline(orchestrator):
    """Test full orchestrator pipeline."""
    result = orchestrator.process_query("What projects have you worked on?")
    
    assert "response" in result
    assert "intent" in result
    assert "total_time" in result
    assert result["total_time"] > 0


def test_orchestrator_with_evaluation(orchestrator):
    """Test orchestrator with evaluation enabled."""
    result = orchestrator.process_query(
        "Tell me about your skills",
        enable_evaluation=True
    )
    
    assert "response" in result
    assert "evaluation" in result or "agents_used" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
