"""Unit tests for LLM providers."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from src.ai_agent.models import ModelConfig
from src.ai_agent.llm import OpenAIProvider, AnthropicProvider, TokenTracker


class TestOpenAIProvider:
    """Test OpenAI provider."""
    
    def test_openai_provider_initialization(self):
        """Test OpenAI provider can be initialized."""
        config = ModelConfig(provider="openai", model_name="gpt-4")
        provider = OpenAIProvider(config, "test_api_key")
        
        assert provider.config == config
        assert provider.api_key == "test_api_key"
    
    @patch('src.ai_agent.llm.openai_provider.OpenAI')
    def test_openai_generate(self, mock_openai_class):
        """Test OpenAI text generation."""
        # Mock the OpenAI client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Mock the response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Generated text"
        mock_client.chat.completions.create.return_value = mock_response
        
        config = ModelConfig(provider="openai")
        provider = OpenAIProvider(config, "test_key")
        
        result = provider.generate("Test prompt")
        
        assert result == "Generated text"
        mock_client.chat.completions.create.assert_called_once()
    
    def test_openai_count_tokens(self):
        """Test token counting."""
        config = ModelConfig(provider="openai")
        provider = OpenAIProvider(config, "test_key")
        
        # Should return a positive number
        count = provider.count_tokens("Hello world")
        assert count > 0
        assert isinstance(count, int)
    
    def test_openai_get_cost(self):
        """Test cost calculation."""
        config = ModelConfig(provider="openai", model_name="gpt-4")
        provider = OpenAIProvider(config, "test_key")
        
        cost = provider.get_cost(1000)
        assert cost > 0
        assert isinstance(cost, float)


class TestAnthropicProvider:
    """Test Anthropic provider."""
    
    def test_anthropic_provider_initialization(self):
        """Test Anthropic provider can be initialized."""
        config = ModelConfig(provider="anthropic", model_name="claude-3-sonnet")
        provider = AnthropicProvider(config, "test_api_key")
        
        assert provider.config == config
        assert provider.api_key == "test_api_key"
    
    @patch('src.ai_agent.llm.anthropic_provider.Anthropic')
    def test_anthropic_generate(self, mock_anthropic_class):
        """Test Anthropic text generation."""
        # Mock the Anthropic client
        mock_client = Mock()
        mock_anthropic_class.return_value = mock_client
        
        # Mock the response
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "Generated text"
        mock_client.messages.create.return_value = mock_response
        
        config = ModelConfig(provider="anthropic")
        provider = AnthropicProvider(config, "test_key")
        
        result = provider.generate("Test prompt")
        
        assert result == "Generated text"
        mock_client.messages.create.assert_called_once()
    
    def test_anthropic_count_tokens(self):
        """Test token counting."""
        config = ModelConfig(provider="anthropic")
        provider = AnthropicProvider(config, "test_key")
        
        count = provider.count_tokens("Hello world")
        assert count > 0
        assert isinstance(count, int)
    
    def test_anthropic_get_cost(self):
        """Test cost calculation."""
        config = ModelConfig(provider="anthropic", model_name="claude-3-sonnet")
        provider = AnthropicProvider(config, "test_key")
        
        cost = provider.get_cost(1000)
        assert cost > 0
        assert isinstance(cost, float)


class TestTokenTracker:
    """Test token tracker."""
    
    def test_token_tracker_initialization(self):
        """Test token tracker initialization."""
        tracker = TokenTracker()
        
        assert tracker.total_tokens == 0
        assert tracker.total_cost == 0.0
        assert len(tracker.usage_records) == 0
    
    def test_record_usage(self):
        """Test recording token usage."""
        tracker = TokenTracker()
        
        tracker.record_usage(
            model="gpt-4",
            prompt_tokens=100,
            completion_tokens=50,
            cost=0.01,
            session_id="session_123",
            user_id="user_456",
        )
        
        assert tracker.total_tokens == 150
        assert tracker.total_cost == 0.01
        assert len(tracker.usage_records) == 1
    
    def test_get_usage_by_session(self):
        """Test getting usage by session."""
        tracker = TokenTracker()
        
        tracker.record_usage("gpt-4", 100, 50, 0.01, session_id="session_1")
        tracker.record_usage("gpt-4", 200, 100, 0.02, session_id="session_2")
        tracker.record_usage("gpt-4", 150, 75, 0.015, session_id="session_1")
        
        session_1_usage = tracker.get_usage_by_session("session_1")
        assert len(session_1_usage) == 2
    
    def test_get_cost_by_model(self):
        """Test getting cost breakdown by model."""
        tracker = TokenTracker()
        
        tracker.record_usage("gpt-4", 100, 50, 0.01)
        tracker.record_usage("gpt-3.5-turbo", 200, 100, 0.005)
        tracker.record_usage("gpt-4", 150, 75, 0.015)
        
        costs = tracker.get_cost_by_model()
        assert costs["gpt-4"] == 0.025
        assert costs["gpt-3.5-turbo"] == 0.005
