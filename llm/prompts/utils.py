from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PromptTemplate:
    template: str

    def format(self, context: Optional[str] = None, **kwargs) -> str:
        fields = {**kwargs}
        if context:
            fields["context"] = self._format_context(context)
        return self.template.format(**fields)

    def _format_context(self, context: str) -> str:
        return f"\nRelevant history: {context}" if context else ""
