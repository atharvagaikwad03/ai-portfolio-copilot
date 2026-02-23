"""FastAPI server for Python backend."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from agents.orchestrator import orchestrator
from rag.vector_store import vector_store
from config.settings import settings
import uvicorn

app = FastAPI(title="AI Portfolio Copilot API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    enable_evaluation: Optional[bool] = None


class ChatResponse(BaseModel):
    session_id: Optional[str]
    response: str
    intent: str
    entities: List[str]
    query_type: str
    confidence: float
    retrieval_used: bool
    retrieval_time: Optional[float]
    num_retrieved_docs: int
    total_time: float
    evaluation: Optional[Dict[str, Any]] = None


class DocumentRequest(BaseModel):
    documents: List[Dict[str, str]]  # [{"content": "...", "metadata": {...}}]
    metadata: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    status: str
    agents: List[str]
    vector_store_stats: Dict[str, Any]


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Portfolio Copilot API", "version": "1.0.0"}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        stats = vector_store.get_stats()
        agent_stats = orchestrator.get_agent_stats()
        return {
            "status": "healthy",
            "agents": agent_stats["agents"],
            "vector_store_stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for processing user queries."""
    try:
        result = orchestrator.process_query(
            user_input=request.message,
            session_id=request.session_id,
            enable_evaluation=request.enable_evaluation
        )
        
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@app.post("/api/documents")
async def add_documents(request: DocumentRequest):
    """Add documents to the vector store."""
    try:
        from langchain_core.documents import Document
        
        documents = [
            Document(
                page_content=doc["content"],
                metadata=doc.get("metadata", {})
            )
            for doc in request.documents
        ]
        
        from rag.retriever import retriever
        num_chunks = retriever.process_and_store_documents(
            documents,
            metadata=request.metadata
        )
        
        return {
            "status": "success",
            "documents_added": len(documents),
            "chunks_created": num_chunks
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding documents: {str(e)}")


@app.get("/api/stats")
async def get_stats():
    """Get system statistics."""
    try:
        agent_stats = orchestrator.get_agent_stats()
        vector_stats = vector_store.get_stats()
        
        return {
            "agents": agent_stats,
            "vector_store": vector_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")


@app.delete("/api/documents")
async def clear_documents():
    """Clear all documents from vector store."""
    try:
        vector_store.delete_all()
        return {"status": "success", "message": "All documents cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing documents: {str(e)}")


if __name__ == "__main__":
    if not settings.validate():
        print("Warning: Some required settings are missing. Check your .env file.")
    
    uvicorn.run(
        "api.server:app",
        host=settings.API_HOST,
        port=settings.PYTHON_API_PORT,
        reload=True
    )
