"""Tool registry."""

from typing import Dict
from ..models import Tool

class ToolRegistry:
    """Registry of available tools."""
    
    def __init__(self):
        """Initialize registry."""
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Tool:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_all(self) -> list:
        """List all tools."""
        return list(self._tools.values())
