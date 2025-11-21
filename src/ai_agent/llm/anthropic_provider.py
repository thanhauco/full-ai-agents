"""Anthropic LLM provider implementation."""

from typing import Iterator

import anthropic
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from ..models import ModelConfig
from .base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic Claude LLM provider."""
    
    def __init__(self, config: ModelConfig, api_key: str):
        """Initialize Anthropic provider.
        
        Args:
            config: Model configuration
            api_key: Anthropic API key
        """
        super().__init__(config, api_key)
        self.client = Anthropic(api_key=api_key)
        self.token_costs = {
            "claude-3-opus": {"input": 0.015 / 1000, "output": 0.075 / 1000},
            "claude-3-sonnet": {"input": 0.003 / 1000, "output": 0.015 / 1000},
            "claude-3-haiku": {"input": 0.00025 / 1000, "output": 0.00125 / 1000},
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def generate(self, prompt: str) -> str:
        """Generate text from prompt.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        try:
            message = self.client.messages.create(
                model=self.config.model_name,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
            )
            
            return message.content[0].text
        
        except anthropic.RateLimitError as e:
            raise
        except anthropic.APIError as e:
            raise
        except Exception as e:
            raise RuntimeError(f"Anthropic API call failed: {str(e)}") from e
    
    def stream_generate(self, prompt: str) -> Iterator[str]:
        """Generate text from prompt with streaming.
        
        Args:
            prompt: Input prompt
            
        Yields:
            Generated text chunks
        """
        try:
            with self.client.messages.stream(
                model=self.config.model_name,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                messages=[{"role": "user", "content": prompt}],
            ) as stream:
                for text in stream.text_stream:
                    yield text
        
        except Exception as e:
            raise RuntimeError(f"Anthropic streaming failed: {str(e)}") from e
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens (estimated)
        """
        # Anthropic uses similar tokenization to GPT
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4
    
    def get_cost(self, tokens: int) -> float:
        """Calculate cost for token count.
        
        Args:
            tokens: Number of tokens
            
        Returns:
            Cost in USD
        """
        model_key = self.config.model_name
        
        if model_key in self.token_costs:
            # Assume average of input and output costs
            avg_cost = (self.token_costs[model_key]["input"] + 
                       self.token_costs[model_key]["output"]) / 2
            return tokens * avg_cost
        
        # Default cost estimate
        return tokens * 0.01 / 1000
