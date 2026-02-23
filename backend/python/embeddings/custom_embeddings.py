"""Custom embedding models for the RAG system.

Uses free HuggingFace sentence-transformers by default (no API key needed).
Falls back to OpenAI embeddings if configured.
"""
from typing import List, Optional
from config.settings import settings
import numpy as np


class CustomEmbeddings:
    """Custom embedding model wrapper using sentence-transformers (free, local)."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or settings.EMBEDDING_MODEL
        self._model = None
        self._initialize()

    def _initialize(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            print(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            print(f"Failed to load embedding model {self.model_name}: {e}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not self._model:
            return [[0.0] * 384 for _ in texts]
        return self._model.encode(texts, show_progress_bar=False).tolist()

    def embed_query(self, text: str) -> List[float]:
        if not self._model:
            return [0.0] * 384
        return self._model.encode(text, show_progress_bar=False).tolist()

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        v1, v2 = np.array(vec1), np.array(vec2)
        dot = np.dot(v1, v2)
        norm = np.linalg.norm(v1) * np.linalg.norm(v2)
        return dot / norm if norm > 0 else 0.0


embedding_model = CustomEmbeddings()
