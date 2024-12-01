import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import chromadb
import numpy as np
from chromadb.config import Settings

from .base import VectorStore


class ChromaStore(VectorStore):
    """Chroma-based vector store implementation."""

    def __init__(
        self, collection_name: str = "running_coach", persist_dir: Optional[str] = None
    ):
        """Initialize ChromaStore.

        Args:
            collection_name: Name of the Chroma collection
            persist_dir: Optional directory for persistent storage. If None, uses in-memory
        """
        settings = Settings()
        if persist_dir:
            settings = Settings(persist_directory=str(Path(persist_dir).resolve()))

        self._client = chromadb.Client(settings)
        self._collection = self._client.get_or_create_collection(name=collection_name)

    async def add(
        self,
        embeddings: Union[np.ndarray, List[float]],
        metadata: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None,
    ) -> str:
        if isinstance(embeddings, np.ndarray):
            embeddings = embeddings.tolist()

        doc_id = id or str(uuid.uuid4())
        self._collection.add(
            embeddings=[embeddings],
            metadatas=[metadata] if metadata else None,
            ids=[doc_id],
        )
        return doc_id

    async def add_many(
        self,
        embeddings: List[Union[np.ndarray, List[float]]],
        metadata: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        embeddings = [
            e.tolist() if isinstance(e, np.ndarray) else e for e in embeddings
        ]
        if not ids:
            ids = [str(uuid.uuid4()) for _ in embeddings]

        self._collection.add(embeddings=embeddings, metadatas=metadata, ids=ids)
        return ids

    async def get(self, id: str) -> Dict[str, Any]:
        result = self._collection.get(ids=[id])
        if not result or not result["ids"]:
            raise KeyError(f"No embedding found with id: {id}")

        return {
            "id": result["ids"][0],
            "embedding": result["embeddings"][0],
            "metadata": result["metadatas"][0] if result["metadatas"] else None,
        }

    async def update(
        self,
        id: str,
        embedding: Optional[Union[np.ndarray, List[float]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        try:
            current = await self.get(id)
        except KeyError:
            raise KeyError(f"Cannot update: no embedding found with id: {id}")

        if isinstance(embedding, np.ndarray):
            embedding = embedding.tolist()

        self._collection.update(
            ids=[id],
            embeddings=[embedding] if embedding else [current["embedding"]],
            metadatas=[metadata] if metadata else [current["metadata"]],
        )

    async def delete(self, id: str) -> None:
        try:
            await self.get(id)  # Check existence
            self._collection.delete(ids=[id])
        except KeyError:
            raise KeyError(f"Cannot delete: no embedding found with id: {id}")

    async def search(
        self,
        query_embedding: Union[np.ndarray, List[float]],
        limit: int = 10,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        if isinstance(query_embedding, np.ndarray):
            query_embedding = query_embedding.tolist()

        results = self._collection.query(
            query_embeddings=[query_embedding], n_results=limit, where=metadata_filter
        )

        return [
            {
                "id": id,
                "embedding": embedding,
                "metadata": metadata if metadata else None,
                "distance": distance,
            }
            for id, embedding, metadata, distance in zip(
                results["ids"][0],
                results["embeddings"][0],
                results["metadatas"][0]
                if results["metadatas"]
                else [None] * len(results["ids"][0]),
                results["distances"][0],
            )
        ]

    async def clear(self) -> None:
        self._collection.delete()
        self._collection = self._client.get_or_create_collection(
            name=self._collection.name
        )
