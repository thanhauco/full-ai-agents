"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import Iterator

from ..models import ModelConfig


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, config: ModelConfig, api_key: str):
        """Initialize LLM provider.
        
        Args:
            config: Model configuration
            api_key: API key for authentication
        """
        self.config = config
        self.api_key = api_key
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from prompt.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def stream_generate(self, prompt: str) -> Iterator[str]:
        """Generate text from prompt with streaming.
        
        Args:
            prompt: Input prompt
            
        Yields:
            Generated text chunks
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        pass
    
    @abstractmethod
    def get_cost(self, tokens: int) -> float:
        """Calculate cost for token count.
        
        Args:
            tokens: Number of tokens
            
        Returns:
            Cost in USD
        """
        pass
