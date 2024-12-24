import os
from typing import AsyncIterator, List, Optional

import google.generativeai as genai
from google.generativeai.types import GenerateContentResponse

from .base import LLMProvider, LLMResponse


class GeminiProvider(LLMProvider):
    """Google Gemini implementation"""

    def __init__(self, model: str = "gemini-pro"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    async def generate(
        self, prompt: str, context: Optional[List[str]] = None
    ) -> LLMResponse:
        """Generate response using Gemini"""
        full_prompt = self._build_prompt(prompt, context)
        response: GenerateContentResponse = await self.model.generate_content_async(
            full_prompt
        )

        return LLMResponse(
            content=response.text,
            raw_response=response,
            usage={"total_tokens": response.usage.total_tokens},
        )

    async def stream(
        self, prompt: str, context: Optional[List[str]] = None
    ) -> AsyncIterator[str]:
        """Stream response using Gemini"""
        full_prompt = self._build_prompt(prompt, context)
        async for chunk in self.model.generate_content_async(full_prompt, stream=True):
            if chunk.text:
                yield chunk.text

    def _build_prompt(self, prompt: str, context: Optional[List[str]] = None) -> str:
        """Build full prompt with context"""
        if not context:
            return prompt

        context_str = "\n".join(context)
        return f"""Context:
{context_str}

Based on the above context, please respond to:
{prompt}"""
