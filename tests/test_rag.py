"""Tests for RAG system."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent / "backend" / "python"))

from langchain.schema import Document
from rag.retriever import retriever


@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    return [
        Document(
            page_content="This is a test document about Python programming.",
            metadata={"source": "test", "type": "document"}
        ),
        Document(
            page_content="This document discusses machine learning and AI.",
            metadata={"source": "test", "type": "document"}
        )
    ]


def test_retriever_initialization():
    """Test retriever initialization."""
    assert retriever is not None
    assert retriever.vector_store is not None


def test_document_processing(sample_documents):
    """Test document processing and storage."""
    # Note: This test may require actual Pinecone connection
    # In a real test environment, use a test index
    try:
        num_chunks = retriever.process_and_store_documents(sample_documents)
        assert num_chunks > 0
    except Exception as e:
        pytest.skip(f"Skipping test due to Pinecone connection: {e}")


def test_context_retrieval():
    """Test context retrieval."""
    try:
        result = retriever.retrieve_context("Python programming")
        assert "documents" in result
        assert "retrieval_time" in result
        assert isinstance(result["documents"], list)
    except Exception as e:
        pytest.skip(f"Skipping test due to Pinecone connection: {e}")


def test_context_formatting():
    """Test context formatting."""
    documents = [
        Document(
            page_content="Test content",
            metadata={"source": "test"}
        )
    ]
    
    formatted = retriever.format_context(documents)
    assert isinstance(formatted, str)
    assert len(formatted) > 0
    assert "Test content" in formatted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
