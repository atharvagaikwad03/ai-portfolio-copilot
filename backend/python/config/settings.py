"""Configuration settings for the AI Portfolio Copilot."""
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from typing import Optional

# Walk up from this file to find .env at the project root
_env_file = find_dotenv(usecwd=True)
if not _env_file:
    # Fallback: explicit path from this file -> config -> python -> backend -> root
    _env_file = str(Path(__file__).resolve().parents[3] / ".env")
load_dotenv(dotenv_path=_env_file, override=True)

# Disable LangSmith tracing if key is a placeholder
if os.getenv("LANGCHAIN_API_KEY", "").startswith("your_"):
    os.environ["LANGCHAIN_TRACING_V2"] = "false"


class Settings:
    """Application settings loaded from environment variables."""
    
    # LLM Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Pinecone Configuration
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "portfolio-copilot")
    
    # Server Configuration
    PYTHON_API_PORT: int = int(os.getenv("PYTHON_API_PORT", "8000"))
    NODE_API_PORT: int = int(os.getenv("NODE_API_PORT", "3000"))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    
    # Evaluation Configuration
    EVAL_MODE: bool = os.getenv("EVAL_MODE", "true").lower() == "true"
    EVAL_THRESHOLD: float = float(os.getenv("EVAL_THRESHOLD", "0.95"))
    EVAL_INTENT_THRESHOLD: float = float(os.getenv("EVAL_INTENT_THRESHOLD", "0.95"))
    
    # LangSmith Configuration
    LANGCHAIN_API_KEY: Optional[str] = os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "portfolio-copilot")
    
    # RAG Configuration
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "5"))
    CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "portfolio")
    
    # Agent Configuration
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    MAX_TOOL_CALLS: int = int(os.getenv("MAX_TOOL_CALLS", "5"))
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present."""
        required = [
            cls.OPENAI_API_KEY,
            cls.PINECONE_API_KEY,
        ]
        return all(required)


settings = Settings()
