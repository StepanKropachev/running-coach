from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VectorStore(ABC):
    @abstractmethod
    async def store(
        self, texts: List[str], metadata: List[Dict[str, Any]] = None
    ) -> None:
        """Store texts and their metadata in the vector store."""
        pass

    @abstractmethod
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar texts in the vector store."""
        pass
