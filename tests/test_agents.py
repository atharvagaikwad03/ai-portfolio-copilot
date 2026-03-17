"""Tests for agent system."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "backend" / "python"))

from agents.base_agent import BaseAgent
from agents.query_agent import QueryAgent
from agents.response_agent import ResponseAgent
from agents.orchestrator import AgentOrchestrator


@pytest.fixture(autouse=True)
def reset_base_agent_state():
    """Reset shared fallback state between tests."""
    BaseAgent._global_llm_disabled_reason = None
    yield
    BaseAgent._global_llm_disabled_reason = None


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


def test_query_agent_local_fallback(monkeypatch, query_agent):
    """Test local intent classification when LLM access fails."""
    def raise_quota_error(messages):
        raise RuntimeError("insufficient_quota")

    monkeypatch.setattr(query_agent, "_invoke_llm", raise_quota_error)

    result = query_agent.process("Tell me about your projects")

    assert result["intent"] == "project_inquiry"
    assert result["requires_retrieval"] is False
    assert result["query_type"] == "project-related"


def test_response_agent_local_fallback_hides_provider_errors(monkeypatch, response_agent):
    """Test local response fallback without leaking provider errors to users."""
    def raise_quota_error(messages):
        raise RuntimeError("insufficient_quota")

    monkeypatch.setattr(response_agent, "_invoke_llm", raise_quota_error)

    result = response_agent.process("What skills does Atharva have?")

    assert result["success"] is True
    assert result["fallback_used"] is True
    assert "insufficient_quota" not in result["response"]
    assert "skills include" in result["response"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
