"""Unit tests for configuration loading."""

import os

import pytest

from src.ai_agent.config import Settings, get_settings, reload_settings
from src.ai_agent.models import AgentConfig, ModelConfig


class TestSettings:
    """Test Settings configuration."""
    
    def test_settings_defaults(self):
        """Test Settings with default values."""
        settings = Settings()
        
        assert settings.api_host == "0.0.0.0"
        assert settings.api_port == 8000
        assert settings.log_level == "INFO"
        assert settings.enable_tools is True
    
    def test_settings_from_env(self, monkeypatch):
        """Test Settings loading from environment variables."""
        monkeypatch.setenv("API_HOST", "127.0.0.1")
        monkeypatch.setenv("API_PORT", "9000")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")
        
        settings = Settings()
        
        assert settings.api_host == "127.0.0.1"
        assert settings.api_port == 9000
        assert settings.log_level == "DEBUG"
    
    def test_settings_get_agent_config(self):
        """Test getting AgentConfig from Settings."""
        settings = Settings(
            max_reasoning_steps=5,
            enable_tools=False,
        )
        
        agent_config = settings.get_agent_config()
        
        assert isinstance(agent_config, AgentConfig)
        assert agent_config.max_reasoning_steps == 5
        assert agent_config.enable_tools is False
    
    def test_settings_get_model_config(self):
        """Test getting ModelConfig from Settings."""
        settings = Settings(
            default_model_provider="anthropic",
            default_model_name="claude-3",
            model_temperature=0.5,
        )
        
        model_config = settings.get_model_config()
        
        assert isinstance(model_config, ModelConfig)
        assert model_config.provider == "anthropic"
        assert model_config.model_name == "claude-3"
        assert model_config.temperature == 0.5
    
    def test_settings_api_keys(self, monkeypatch):
        """Test API key configuration."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_anthropic_key")
        
        settings = Settings()
        
        assert settings.openai_api_key == "test_openai_key"
        assert settings.anthropic_api_key == "test_anthropic_key"
    
    def test_settings_redis_config(self, monkeypatch):
        """Test Redis configuration."""
        monkeypatch.setenv("REDIS_HOST", "redis.example.com")
        monkeypatch.setenv("REDIS_PORT", "6380")
        monkeypatch.setenv("REDIS_DB", "1")
        
        settings = Settings()
        
        assert settings.redis_host == "redis.example.com"
        assert settings.redis_port == 6380
        assert settings.redis_db == 1
    
    def test_settings_rate_limiting(self):
        """Test rate limiting configuration."""
        settings = Settings(
            rate_limit_per_minute=100,
            rate_limit_per_hour=5000,
        )
        
        assert settings.rate_limit_per_minute == 100
        assert settings.rate_limit_per_hour == 5000


class TestGlobalSettings:
    """Test global settings functions."""
    
    def test_get_settings_singleton(self):
        """Test that get_settings returns same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        
        assert settings1 is settings2
    
    def test_reload_settings(self, monkeypatch):
        """Test reloading settings."""
        # Get initial settings
        settings1 = get_settings()
        initial_host = settings1.api_host
        
        # Change environment
        monkeypatch.setenv("API_HOST", "new.host.com")
        
        # Reload settings
        settings2 = reload_settings()
        
        # Should be different instance with new values
        assert settings2 is not settings1
        assert settings2.api_host == "new.host.com"
