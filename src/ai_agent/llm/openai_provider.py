"""OpenAI LLM provider implementation."""

import time
from typing import Iterator

import openai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from ..models import ModelConfig
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(self, config: ModelConfig, api_key: str):
        """Initialize OpenAI provider.
        
        Args:
            config: Model configuration
            api_key: OpenAI API key
        """
        super().__init__(config, api_key)
        self.client = OpenAI(api_key=api_key)
        self.token_costs = {
            "gpt-4": {"input": 0.03 / 1000, "output": 0.06 / 1000},
            "gpt-4-turbo": {"input": 0.01 / 1000, "output": 0.03 / 1000},
            "gpt-3.5-turbo": {"input": 0.0005 / 1000, "output": 0.0015 / 1000},
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
            
        Raises:
            openai.APIError: If API call fails
            openai.RateLimitError: If rate limit is exceeded
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                frequency_penalty=self.config.frequency_penalty,
                presence_penalty=self.config.presence_penalty,
            )
            
            return response.choices[0].message.content or ""
        
        except openai.RateLimitError as e:
            # Re-raise rate limit errors for retry
            raise
        except openai.APIError as e:
            # Re-raise API errors for retry
            raise
        except Exception as e:
            # Wrap other exceptions
            raise RuntimeError(f"OpenAI API call failed: {str(e)}") from e
    
    def stream_generate(self, prompt: str) -> Iterator[str]:
        """Generate text from prompt with streaming.
        
        Args:
            prompt: Input prompt
            
        Yields:
            Generated text chunks
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            raise RuntimeError(f"OpenAI streaming failed: {str(e)}") from e
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens
        """
        try:
            import tiktoken
            
            # Get encoding for model
            if "gpt-4" in self.config.model_name:
                encoding = tiktoken.encoding_for_model("gpt-4")
            elif "gpt-3.5" in self.config.model_name:
                encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
            else:
                encoding = tiktoken.get_encoding("cl100k_base")
            
            return len(encoding.encode(text))
        
        except Exception:
            # Fallback: rough estimate (1 token ≈ 4 characters)
            return len(text) // 4
    
    def get_cost(self, tokens: int) -> float:
        """Calculate cost for token count.
        
        Args:
            tokens: Number of tokens
            
        Returns:
            Cost in USD
        """
        model_base = self.config.model_name.split("-")[0:2]
        model_key = "-".join(model_base)
        
        if model_key in self.token_costs:
            # Assume average of input and output costs
            avg_cost = (self.token_costs[model_key]["input"] + 
                       self.token_costs[model_key]["output"]) / 2
            return tokens * avg_cost
        
        # Default cost estimate
        return tokens * 0.01 / 1000
