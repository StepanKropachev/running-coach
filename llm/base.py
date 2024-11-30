from abc import ABC, abstractmethod
from typing import Any, Dict


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Generate text based on prompt and context."""
        pass
