from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union

import numpy as np


class VectorStore(ABC):
    """Abstract base class for vector store implementations."""

    @abstractmethod
    async def add(
        self,
        embeddings: Union[np.ndarray, List[float]],
        metadata: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None,
    ) -> str:
        """Add a single embedding with optional metadata to the store.

        Args:
            embeddings: Vector embedding as numpy array or list of floats
            metadata: Optional metadata associated with the embedding
            id: Optional unique identifier. If not provided, will be auto-generated

        Returns:
            str: Unique identifier of the stored embedding
        """
        pass

    @abstractmethod
    async def add_many(
        self,
        embeddings: List[Union[np.ndarray, List[float]]],
        metadata: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Add multiple embeddings with optional metadata to the store.

        Args:
            embeddings: List of vector embeddings
            metadata: Optional list of metadata dicts for each embedding
            ids: Optional list of unique identifiers

        Returns:
            List[str]: List of unique identifiers for stored embeddings
        """
        pass

    @abstractmethod
    async def get(self, id: str) -> Dict[str, Any]:
        """Retrieve a single embedding by ID.

        Args:
            id: Unique identifier of the embedding

        Returns:
            Dict containing embedding vector and metadata

        Raises:
            KeyError: If ID not found
        """
        pass

    @abstractmethod
    async def update(
        self,
        id: str,
        embedding: Optional[Union[np.ndarray, List[float]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update an existing embedding or its metadata.

        Args:
            id: Unique identifier of the embedding to update
            embedding: Optional new embedding vector
            metadata: Optional new or updated metadata

        Raises:
            KeyError: If ID not found
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete an embedding by ID.

        Args:
            id: Unique identifier of the embedding to delete

        Raises:
            KeyError: If ID not found
        """
        pass

    @abstractmethod
    async def search(
        self,
        query_embedding: Union[np.ndarray, List[float]],
        limit: int = 10,
        metadata_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar embeddings.

        Args:
            query_embedding: Query vector to search for
            limit: Maximum number of results to return
            metadata_filter: Optional filter to apply on metadata

        Returns:
            List of dicts containing matched embeddings and their metadata,
            sorted by similarity score (descending)
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Remove all embeddings from the store."""
        pass
