"""Tool executor with retry logic."""

from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Any, Dict

class ToolExecutor:
    """Execute tools with retry logic."""
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def execute(self, tool_func: callable, params: Dict[str, Any]) -> Any:
        """Execute tool with retry."""
        return tool_func(**params)
