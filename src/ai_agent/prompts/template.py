"""Prompt template with variable substitution."""

import re
from typing import Any, Dict, List


class PromptTemplate:
    """Template for prompts with variable substitution."""
    
    def __init__(
        self,
        name: str,
        template: str,
        variables: List[str],
        role: str = "assistant",
        guardrails: List[str] = None,
    ):
        """Initialize prompt template.
        
        Args:
            name: Template name
            template: Template string with {variable} placeholders
            variables: List of variable names
            role: Agent role/persona
            guardrails: List of guardrails (do's and don'ts)
        """
        self.name = name
        self.template = template
        self.variables = variables
        self.role = role
        self.guardrails = guardrails or []
    
    def render(self, **kwargs: Any) -> str:
        """Render template with variable values.
        
        Args:
            **kwargs: Variable values
            
        Returns:
            Rendered template string
            
        Raises:
            ValueError: If required variables are missing
        """
        # Check for missing variables
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")
        
        # Substitute variables
        rendered = self.template
        for var, value in kwargs.items():
            rendered = rendered.replace(f"{{{var}}}", str(value))
        
        return rendered
    
    def get_full_prompt(self, **kwargs: Any) -> str:
        """Get full prompt with role and guardrails.
        
        Args:
            **kwargs: Variable values
            
        Returns:
            Full prompt string
        """
        parts = []
        
        # Add role
        if self.role:
            parts.append(f"You are a {self.role}.")
        
        # Add guardrails
        if self.guardrails:
            parts.append("\nGuidelines:")
            for guardrail in self.guardrails:
                parts.append(f"- {guardrail}")
        
        # Add rendered template
        parts.append("\n" + self.render(**kwargs))
        
        return "\n".join(parts)
