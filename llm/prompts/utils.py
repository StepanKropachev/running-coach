from typing import Dict, List, Optional

import google.generativeai as genai


class ContextInjector:
    MAX_TOKENS = 30720  # Gemini's context window

    def __init__(self, template: str):
        self.template = template
        self.token_count = 0

    def _count_tokens(self, text: str) -> int:
        # Simple token counting for Gemini
        return len(text.split())

    def _truncate_context(self, context: List[str], max_tokens: int) -> List[str]:
        truncated = []
        current_tokens = 0

        for item in context:
            tokens = self._count_tokens(item)
            if current_tokens + tokens <= max_tokens:
                truncated.append(item)
                current_tokens += tokens
            else:
                break

        return truncated

    def inject(
        self, context: List[str], variables: Optional[Dict[str, str]] = None
    ) -> str:
        max_context_tokens = int(self.MAX_TOKENS * 0.8)

        truncated_context = self._truncate_context(context, max_context_tokens)

        context_str = "\n".join(truncated_context)

        variables = variables or {}
        variables["context"] = context_str

        return self.template.format(**variables)
