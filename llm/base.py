from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Dict, List, Optional


@dataclass
class LLMResponse:
    """Standardized response from any LLM provider"""

    content: str
    raw_response: Optional[any] = None
    usage: Optional[Dict[str, int]] = None


class LLMProvider(ABC):
    """Base class for LLM providers"""

    @abstractmethod
    async def generate(
        self, prompt: str, context: Optional[List[str]] = None
    ) -> LLMResponse:
        """Generate LLM response from prompt and optional context"""
        pass

    @abstractmethod
    async def stream(
        self, prompt: str, context: Optional[List[str]] = None
    ) -> AsyncIterator[str]:
        """Stream LLM response"""
        pass
