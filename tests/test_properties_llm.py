"""Property-based tests for LLM providers.

Feature: ai-agent-system
Property 2: LLM authentication consistency - Validates: Requirements 3.2
Property 3: Token usage tracking - Validates: Requirements 3.3
Property 5: LLM error handling - Validates: Requirements 3.5
"""

from hypothesis import given, strategies as st
from unittest.mock import Mock, patch
import pytest

from src.ai_agent.models import ModelConfig
from src.ai_agent.llm import OpenAIProvider, AnthropicProvider, TokenTracker


class TestLLMAuthenticationConsistency:
    """Property 2: LLM authentication consistency.
    
    For any LLM API call, the system should include valid authentication
    credentials in the request headers.
    """
    
    @given(
        api_key=st.text(min_size=10, max_size=100),
        prompt=st.text(min_size=1, max_size=500),
    )
    @patch('src.ai_agent.llm.openai_provider.OpenAI')
    def test_openai_authentication_included(self, mock_openai_class, api_key: str, prompt: str):
        """Test that OpenAI provider includes authentication in all calls."""
        # Mock the client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Mock response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "response"
        mock_client.chat.completions.create.return_value = mock_response
        
        config = ModelConfig(provider="openai")
        provider = OpenAIProvider(config, api_key)
        
        # Verify the client was initialized with the API key
        mock_openai_class.assert_called_once_with(api_key=api_key)
        
        # Make a call
        provider.generate(prompt)
        
        # Verify the call was made (authentication is handled by the client)
        assert mock_client.chat.completions.create.called
    
    @given(
        api_key=st.text(min_size=10, max_size=100),
        prompt=st.text(min_size=1, max_size=500),
    )
    @patch('src.ai_agent.llm.anthropic_provider.Anthropic')
    def test_anthropic_authentication_included(self, mock_anthropic_class, api_key: str, prompt: str):
        """Test that Anthropic provider includes authentication in all calls."""
        # Mock the client
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        
        # Mock response
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "response"
        mock_client.messages.create.return_value = mock_response
        
        config = ModelConfig(provider="anthropic")
        provider = AnthropicProvider(config, api_key)
        
        # Verify the client was initialized with the API key
        mock_anthropic_class.assert_called_once_with(api_key=api_key)
        
        # Make a call
        provider.generate(prompt)
        
        # Verify the call was made
        assert mock_client.messages.create.called


class TestTokenUsageTracking:
    """Property 3: Token usage tracking.
    
    For any LLM API call, the system should record the token count used in that call.
    """
    
    @given(
        prompt_tokens=st.integers(min_value=1, max_value=10000),
        completion_tokens=st.integers(min_value=1, max_value=10000),
        cost=st.floats(min_value=0.0001, max_value=10.0, allow_nan=False, allow_infinity=False),
    )
    def test_token_tracking_records_usage(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
    ):
        """Test that token tracker records all usage."""
        tracker = TokenTracker()
        initial_total = tracker.total_tokens
        initial_cost = tracker.total_cost
        
        tracker.record_usage(
            model="gpt-4",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost,
        )
        
        # Verify tokens are tracked
        assert tracker.total_tokens == initial_total + prompt_tokens + completion_tokens
        assert tracker.total_cost == initial_cost + cost
        assert len(tracker.usage_records) > 0
    
    @given(
        calls=st.lists(
            st.tuples(
                st.integers(min_value=1, max_value=1000),  # prompt_tokens
                st.integers(min_value=1, max_value=1000),  # completion_tokens
                st.floats(min_value=0.0001, max_value=1.0, allow_nan=False, allow_infinity=False),  # cost
            ),
            min_size=1,
            max_size=10,
        )
    )
    def test_token_tracking_accumulates(self, calls):
        """Test that token tracker accumulates across multiple calls."""
        tracker = TokenTracker()
        
        expected_tokens = 0
        expected_cost = 0.0
        
        for prompt_tokens, completion_tokens, cost in calls:
            tracker.record_usage(
                model="gpt-4",
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost=cost,
            )
            expected_tokens += prompt_tokens + completion_tokens
            expected_cost += cost
        
        # Verify accumulation
        assert tracker.total_tokens == expected_tokens
        assert abs(tracker.total_cost - expected_cost) < 0.0001  # Float comparison
        assert len(tracker.usage_records) == len(calls)


class TestLLMErrorHandling:
    """Property 5: LLM error handling.
    
    For any LLM API error (rate limit, timeout, invalid request), the system
    should handle it gracefully without crashing.
    """
    
    @patch('src.ai_agent.llm.openai_provider.OpenAI')
    def test_openai_handles_api_errors(self, mock_openai_class):
        """Test that OpenAI provider handles API errors gracefully."""
        import openai
        
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Simulate API error
        mock_client.chat.completions.create.side_effect = openai.APIError("API Error")
        
        config = ModelConfig(provider="openai")
        provider = OpenAIProvider(config, "test_key")
        
        # Should raise an exception but not crash
        with pytest.raises((openai.APIError, RuntimeError)):
            provider.generate("test prompt")
    
    @patch('src.ai_agent.llm.openai_provider.OpenAI')
    def test_openai_handles_rate_limit(self, mock_openai_class):
        """Test that OpenAI provider handles rate limit errors."""
        import openai
        
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Simulate rate limit error
        mock_client.chat.completions.create.side_effect = openai.RateLimitError("Rate limit")
        
        config = ModelConfig(provider="openai")
        provider = OpenAIProvider(config, "test_key")
        
        # Should raise an exception but not crash
        with pytest.raises(openai.RateLimitError):
            provider.generate("test prompt")
    
    @patch('src.ai_agent.llm.anthropic_provider.Anthropic')
    def test_anthropic_handles_api_errors(self, mock_anthropic_class):
        """Test that Anthropic provider handles API errors gracefully."""
        import anthropic
        
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        
        # Simulate API error
        mock_client.messages.create.side_effect = anthropic.APIError("API Error")
        
        config = ModelConfig(provider="anthropic")
        provider = AnthropicProvider(config, "test_key")
        
        # Should raise an exception but not crash
        with pytest.raises((anthropic.APIError, RuntimeError)):
            provider.generate("test prompt")
