"""Configuration loader from environment variables."""

import os
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

from .models import AgentConfig, ModelConfig


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Provider Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Vector Database Configuration
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "ai-agent-memory"
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0
    
    # Database Configuration
    database_url: Optional[str] = None
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60
    
    # Monitoring Configuration
    log_level: str = "INFO"
    enable_metrics: bool = True
    prometheus_port: int = 9090
    
    # Agent Configuration
    max_reasoning_steps: int = 10
    enable_tools: bool = True
    enable_memory: bool = True
    enable_safety_filter: bool = True
    cache_responses: bool = True
    parallel_tool_execution: bool = False
    
    # Model Configuration
    default_model_provider: str = "openai"
    default_model_name: str = "gpt-4"
    model_temperature: float = 0.7
    model_max_tokens: int = 2000
    
    # Multimodal Configuration
    enable_multimodal: bool = False
    whisper_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    rate_limit_per_hour: int = 1000
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def get_agent_config(self) -> AgentConfig:
        """Get AgentConfig from settings.
        
        Returns:
            AgentConfig instance with current settings
        """
        model_config = ModelConfig(
            provider=self.default_model_provider,
            model_name=self.default_model_name,
            temperature=self.model_temperature,
            max_tokens=self.model_max_tokens,
        )
        
        return AgentConfig(
            model_config=model_config,
            max_reasoning_steps=self.max_reasoning_steps,
            enable_tools=self.enable_tools,
            enable_memory=self.enable_memory,
            enable_safety_filter=self.enable_safety_filter,
            cache_responses=self.cache_responses,
            parallel_tool_execution=self.parallel_tool_execution,
        )
    
    def get_model_config(self) -> ModelConfig:
        """Get ModelConfig from settings.
        
        Returns:
            ModelConfig instance with current settings
        """
        return ModelConfig(
            provider=self.default_model_provider,
            model_name=self.default_model_name,
            temperature=self.model_temperature,
            max_tokens=self.model_max_tokens,
        )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance.
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from environment.
    
    Returns:
        New Settings instance
    """
    global _settings
    _settings = Settings()
    return _settings
