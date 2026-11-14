"""Store and search vectors using persistent vector storage (ChromaDB / pgvector)."""
from pathlib import Path
from typing import Any
import chromadb
from .models import Chunk


class ChromaVectorStore:
    """Persistent vector database using ChromaDB with cosine distance."""

    def __init__(self, persist_directory: str = "starter/data/chroma_db", dimensions: int = 384) -> None:
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.dimensions = dimensions
        self.client = chromadb.PersistentClient(path=str(self.persist_directory))
        print(f"[VectorStore] Initialized ChromaDB at {self.persist_directory}")

    def _get_collection(self, strategy: str):
        collection_name = f"ingestion_strategy_{strategy.lower()}"
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def create_schema(self) -> None:
        """Initialize collections for Strategy A, B, and C."""
        for strat in ["a", "b", "c"]:
            self._get_collection(strat)
        print("[VectorStore] Schema created for strategies A, B, C.")

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        """Validate lengths/dimensions and write stable IDs without duplicates."""
        if len(chunks) != len(vectors):
            raise ValueError(f"Chunks count ({len(chunks)}) does not match vectors count ({len(vectors)})")

        collection = self._get_collection(strategy)
        
        # Clear existing entries in collection to ensure idempotent ingestion
        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)

        if not chunks:
            return

        ids = [c.chunk_id for c in chunks]
        documents = [c.text for c in chunks]
        metadatas = []
        for c in chunks:
            m = {
                "document_id": c.document_id,
                "source": c.source,
                "page": int(c.page),
                "strategy": strategy.upper()
            }
            # Flatten optional metadata for Chroma
            for k, v in c.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    m[k] = v
            metadatas.append(m)

        collection.add(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas
        )
        print(f"[VectorStore] Successfully upserted {len(chunks)} chunks into strategy {strategy.upper()}.")

    def search(
        self,
        strategy: str,
        query_vector: list[float],
        top_k: int = 3,
        filters: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Filter permitted metadata, rank by cosine similarity, return top-k."""
        collection = self._get_collection(strategy)
        
        where_clause = None
        if filters:
            # Build valid where clause
            if len(filters) == 1:
                k, v = next(iter(filters.items()))
                where_clause = {k: v}
            else:
                where_clause = {"$and": [{k: v} for k, v in filters.items()]}

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=top_k,
            where=where_clause,
            include=["documents", "metadatas", "distances"]
        )

        hits: list[dict[str, Any]] = []
        if not results["ids"] or not results["ids"][0]:
            return hits

        ids = results["ids"][0]
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        for chunk_id, doc, meta, dist in zip(ids, docs, metas, distances):
            # Cosine similarity score = 1 - cosine distance
            score = 1.0 - float(dist)
            hits.append({
                "chunk_id": chunk_id,
                "document_id": meta.get("document_id", ""),
                "source": meta.get("source", ""),
                "page": meta.get("page", 0),
                "text": doc,
                "score": round(score, 4),
                "metadata": meta
            })

        return hits
