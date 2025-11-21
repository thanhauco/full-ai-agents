"""Property-based tests for configuration validation.

Feature: ai-agent-system, Property 4: Model parameter propagation
Validates: Requirements 3.4
"""

from hypothesis import given, strategies as st
import pytest

from src.ai_agent.models import ModelConfig
from src.ai_agent.config import Settings


class TestModelParameterPropagation:
    """Property 4: Model parameter propagation.
    
    For any set of model configuration parameters, those parameters should be
    correctly passed to the LLM API.
    """
    
    @given(
        provider=st.sampled_from(["openai", "anthropic", "llama"]),
        model_name=st.text(min_size=1, max_size=50),
        temperature=st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False),
        max_tokens=st.integers(min_value=1, max_value=100000),
        top_p=st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False),
        frequency_penalty=st.floats(min_value=-2.0, max_value=2.0, allow_nan=False, allow_infinity=False),
        presence_penalty=st.floats(min_value=-2.0, max_value=2.0, allow_nan=False, allow_infinity=False),
    )
    def test_model_config_parameters_preserved(
        self,
        provider: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
        top_p: float,
        frequency_penalty: float,
        presence_penalty: float,
    ):
        """Test that model configuration parameters are preserved correctly.
        
        Property: For any valid set of model parameters, creating a ModelConfig
        should preserve all parameter values exactly.
        """
        # Create model config with parameters
        config = ModelConfig(
            provider=provider,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
        
        # Verify all parameters are preserved
        assert config.provider == provider.lower()
        assert config.model_name == model_name
        assert config.temperature == temperature
        assert config.max_tokens == max_tokens
        assert config.top_p == top_p
        assert config.frequency_penalty == frequency_penalty
        assert config.presence_penalty == presence_penalty
    
    @given(
        provider=st.sampled_from(["openai", "anthropic", "llama"]),
        model_name=st.text(min_size=1, max_size=50),
        temperature=st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False),
        max_tokens=st.integers(min_value=1, max_value=100000),
    )
    def test_settings_to_model_config_propagation(
        self,
        provider: str,
        model_name: str,
        temperature: float,
        max_tokens: int,
    ):
        """Test that Settings correctly propagates to ModelConfig.
        
        Property: For any valid settings, get_model_config() should return
        a ModelConfig with the same parameter values.
        """
        # Create settings with parameters
        settings = Settings(
            default_model_provider=provider,
            default_model_name=model_name,
            model_temperature=temperature,
            model_max_tokens=max_tokens,
        )
        
        # Get model config from settings
        model_config = settings.get_model_config()
        
        # Verify parameters are propagated correctly
        assert model_config.provider == provider.lower()
        assert model_config.model_name == model_name
        assert model_config.temperature == temperature
        assert model_config.max_tokens == max_tokens
    
    @given(
        max_reasoning_steps=st.integers(min_value=1, max_value=100),
        enable_tools=st.booleans(),
        enable_memory=st.booleans(),
        enable_safety_filter=st.booleans(),
        cache_responses=st.booleans(),
        parallel_tool_execution=st.booleans(),
    )
    def test_settings_to_agent_config_propagation(
        self,
        max_reasoning_steps: int,
        enable_tools: bool,
        enable_memory: bool,
        enable_safety_filter: bool,
        cache_responses: bool,
        parallel_tool_execution: bool,
    ):
        """Test that Settings correctly propagates to AgentConfig.
        
        Property: For any valid agent settings, get_agent_config() should return
        an AgentConfig with the same parameter values.
        """
        # Create settings with parameters
        settings = Settings(
            max_reasoning_steps=max_reasoning_steps,
            enable_tools=enable_tools,
            enable_memory=enable_memory,
            enable_safety_filter=enable_safety_filter,
            cache_responses=cache_responses,
            parallel_tool_execution=parallel_tool_execution,
        )
        
        # Get agent config from settings
        agent_config = settings.get_agent_config()
        
        # Verify parameters are propagated correctly
        assert agent_config.max_reasoning_steps == max_reasoning_steps
        assert agent_config.enable_tools == enable_tools
        assert agent_config.enable_memory == enable_memory
        assert agent_config.enable_safety_filter == enable_safety_filter
        assert agent_config.cache_responses == cache_responses
        assert agent_config.parallel_tool_execution == parallel_tool_execution
    
    @given(
        temperature1=st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False),
        temperature2=st.floats(min_value=0.0, max_value=2.0, allow_nan=False, allow_infinity=False),
    )
    def test_model_config_independence(self, temperature1: float, temperature2: float):
        """Test that ModelConfig instances are independent.
        
        Property: Creating two ModelConfig instances with different parameters
        should not affect each other.
        """
        config1 = ModelConfig(temperature=temperature1)
        config2 = ModelConfig(temperature=temperature2)
        
        # Verify they have their own values
        assert config1.temperature == temperature1
        assert config2.temperature == temperature2
        
        # Modifying one should not affect the other
        config1.temperature = 1.5
        assert config2.temperature == temperature2
