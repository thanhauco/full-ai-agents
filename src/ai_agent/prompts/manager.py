"""Prompt template manager."""

from typing import Dict, Optional

from .template import PromptTemplate


class PromptManager:
    """Manage prompt templates."""
    
    def __init__(self):
        """Initialize prompt manager."""
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_default_templates()
    
    def _load_default_templates(self) -> None:
        """Load default prompt templates."""
        # Default agent template
        self.register_template(
            PromptTemplate(
                name="default_agent",
                template="User request: {request}\n\nPlease provide a helpful response.",
                variables=["request"],
                role="helpful AI assistant",
                guardrails=[
                    "Be helpful, harmless, and honest",
                    "Provide accurate information",
                    "Admit when you don't know something",
                    "Respect user privacy and safety",
                ],
            )
        )
        
        # Reasoning template
        self.register_template(
            PromptTemplate(
                name="reasoning",
                template="Task: {task}\n\nBreak this down into steps and solve it systematically.",
                variables=["task"],
                role="analytical problem solver",
                guardrails=[
                    "Think step by step",
                    "Show your reasoning",
                    "Verify each step",
                ],
            )
        )
    
    def register_template(self, template: PromptTemplate) -> None:
        """Register a prompt template.
        
        Args:
            template: Template to register
        """
        self.templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Get a template by name.
        
        Args:
            name: Template name
            
        Returns:
            Template or None if not found
        """
        return self.templates.get(name)
    
    def list_templates(self) -> list[str]:
        """List all template names.
        
        Returns:
            List of template names
        """
        return list(self.templates.keys())
    
    def delete_template(self, name: str) -> bool:
        """Delete a template.
        
        Args:
            name: Template name
            
        Returns:
            True if deleted, False if not found
        """
        if name in self.templates:
            del self.templates[name]
            return True
        return False
