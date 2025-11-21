"""Prompt renderer with optimization."""

import re
from typing import Any, Dict


class PromptRenderer:
    """Render and optimize prompts."""
    
    @staticmethod
    def render(template: str, variables: Dict[str, Any]) -> str:
        """Render template with variables.
        
        Args:
            template: Template string
            variables: Variable values
            
        Returns:
            Rendered string
        """
        rendered = template
        for key, value in variables.items():
            rendered = rendered.replace(f"{{{key}}}", str(value))
        return rendered
    
    @staticmethod
    def optimize(prompt: str) -> str:
        """Optimize prompt to reduce token count.
        
        Args:
            prompt: Prompt to optimize
            
        Returns:
            Optimized prompt
        """
        # Remove extra whitespace
        optimized = re.sub(r'\s+', ' ', prompt)
        
        # Remove leading/trailing whitespace
        optimized = optimized.strip()
        
        # Remove multiple newlines
        optimized = re.sub(r'\n\s*\n', '\n\n', optimized)
        
        return optimized
    
    @staticmethod
    def count_approximate_tokens(text: str) -> int:
        """Estimate token count.
        
        Args:
            text: Text to count
            
        Returns:
            Approximate token count
        """
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4
