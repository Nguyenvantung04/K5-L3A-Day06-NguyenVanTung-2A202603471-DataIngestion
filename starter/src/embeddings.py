"""Real embedding provider adapter using Sentence Transformers."""
import os
# Force offline mode so huggingface does not make external network calls
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from typing import Protocol
import numpy as np


class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return one vector per input text, in the same order."""
        ...

    def embed_query(self, question: str) -> list[float]:
        """Return a query vector compatible with the stored document vectors."""
        ...


class MyEmbedder:
    """Production embedder using sentence-transformers (all-MiniLM-L6-v2) offline."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        try:
            from sentence_transformers import SentenceTransformer
            # local_files_only=True ensures no network requests
            self._model = SentenceTransformer(model_name, local_files_only=True)
            # Infer dimensions by a dummy test
            test_vec = self._model.encode("test", normalize_embeddings=True)
            self.dimensions = int(test_vec.shape[0])
            print(f"[Embedder] Loaded {model_name} offline with {self.dimensions} dimensions.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize embedding model '{model_name}': {e}")

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Return L2-normalized embeddings for documents."""
        if not texts:
            return []
        vectors = self._model.encode(texts, batch_size=32, show_progress_bar=False, normalize_embeddings=True)
        return [vec.tolist() for vec in vectors]

    def embed_query(self, question: str) -> list[float]:
        """Return L2-normalized query vector."""
        vec = self._model.encode(question, normalize_embeddings=True)
        return vec.tolist()
