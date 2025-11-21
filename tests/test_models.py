"""Unit tests for data models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.ai_agent.models import (
    AgentConfig,
    AgentRequest,
    AgentResponse,
    Memory,
    ModelConfig,
    MultimodalInput,
    MultimodalInputType,
    ParameterSpec,
    ReasoningStep,
    Tool,
    ToolCall,
    UserPreferences,
    UserProfile,
)


class TestModelConfig:
    """Test ModelConfig validation."""
    
    def test_model_config_defaults(self):
        """Test ModelConfig with default values."""
        config = ModelConfig()
        
        assert config.provider == "openai"
        assert config.model_name == "gpt-4"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
    
    def test_model_config_custom_values(self):
        """Test ModelConfig with custom values."""
        config = ModelConfig(
            provider="anthropic",
            model_name="claude-3",
            temperature=0.5,
            max_tokens=4000,
        )
        
        assert config.provider == "anthropic"
        assert config.model_name == "claude-3"
        assert config.temperature == 0.5
        assert config.max_tokens == 4000
    
    def test_model_config_invalid_provider(self):
        """Test that invalid provider raises error."""
        with pytest.raises(ValidationError):
            ModelConfig(provider="invalid_provider")
    
    def test_model_config_temperature_bounds(self):
        """Test temperature validation bounds."""
        # Valid temperatures
        ModelConfig(temperature=0.0)
        ModelConfig(temperature=1.0)
        ModelConfig(temperature=2.0)
        
        # Invalid temperatures
        with pytest.raises(ValidationError):
            ModelConfig(temperature=-0.1)
        
        with pytest.raises(ValidationError):
            ModelConfig(temperature=2.1)
    
    def test_model_config_max_tokens_positive(self):
        """Test that max_tokens must be positive."""
        ModelConfig(max_tokens=1)
        ModelConfig(max_tokens=10000)
        
        with pytest.raises(ValidationError):
            ModelConfig(max_tokens=0)
        
        with pytest.raises(ValidationError):
            ModelConfig(max_tokens=-1)


class TestAgentConfig:
    """Test AgentConfig validation."""
    
    def test_agent_config_defaults(self):
        """Test AgentConfig with defaults."""
        config = AgentConfig()
        
        assert config.max_reasoning_steps == 10
        assert config.enable_tools is True
        assert config.enable_memory is True
        assert config.enable_safety_filter is True
    
    def test_agent_config_custom_values(self):
        """Test AgentConfig with custom values."""
        model_config = ModelConfig(provider="anthropic")
        config = AgentConfig(
            model_config=model_config,
            max_reasoning_steps=5,
            enable_tools=False,
        )
        
        assert config.model_config.provider == "anthropic"
        assert config.max_reasoning_steps == 5
        assert config.enable_tools is False


class TestAgentRequest:
    """Test AgentRequest validation."""
    
    def test_agent_request_valid(self):
        """Test valid AgentRequest."""
        request = AgentRequest(
            session_id="session_123",
            user_id="user_456",
            message="Hello, agent!",
        )
        
        assert request.session_id == "session_123"
        assert request.user_id == "user_456"
        assert request.message == "Hello, agent!"
    
    def test_agent_request_empty_message(self):
        """Test that empty message raises error."""
        with pytest.raises(ValidationError):
            AgentRequest(
                session_id="session_123",
                user_id="user_456",
                message="",
            )
    
    def test_agent_request_whitespace_message(self):
        """Test that whitespace-only message raises error."""
        with pytest.raises(ValidationError):
            AgentRequest(
                session_id="session_123",
                user_id="user_456",
                message="   ",
            )
    
    def test_agent_request_with_context(self):
        """Test AgentRequest with context."""
        request = AgentRequest(
            session_id="session_123",
            user_id="user_456",
            message="Hello",
            context={"key": "value"},
        )
        
        assert request.context == {"key": "value"}
    
    def test_agent_request_with_multimodal(self):
        """Test AgentRequest with multimodal inputs."""
        multimodal_input = MultimodalInput(
            type=MultimodalInputType.IMAGE,
            content="https://example.com/image.jpg",
        )
        
        request = AgentRequest(
            session_id="session_123",
            user_id="user_456",
            message="Analyze this image",
            multimodal_inputs=[multimodal_input],
        )
        
        assert len(request.multimodal_inputs) == 1
        assert request.multimodal_inputs[0].type == MultimodalInputType.IMAGE


class TestAgentResponse:
    """Test AgentResponse model."""
    
    def test_agent_response_basic(self):
        """Test basic AgentResponse."""
        response = AgentResponse(
            session_id="session_123",
            message="Response message",
        )
        
        assert response.session_id == "session_123"
        assert response.message == "Response message"
        assert response.confidence == 1.0
    
    def test_agent_response_with_reasoning_steps(self):
        """Test AgentResponse with reasoning steps."""
        step = ReasoningStep(
            step_number=1,
            description="First step",
            action="analyze",
            result="analysis complete",
            confidence=0.9,
        )
        
        response = AgentResponse(
            session_id="session_123",
            message="Response",
            reasoning_steps=[step],
        )
        
        assert len(response.reasoning_steps) == 1
        assert response.reasoning_steps[0].step_number == 1
    
    def test_agent_response_with_tool_calls(self):
        """Test AgentResponse with tool calls."""
        tool_call = ToolCall(
            tool_name="search",
            parameters={"query": "test"},
            result="search results",
            success=True,
        )
        
        response = AgentResponse(
            session_id="session_123",
            message="Response",
            tool_calls=[tool_call],
        )
        
        assert len(response.tool_calls) == 1
        assert response.tool_calls[0].tool_name == "search"


class TestMemory:
    """Test Memory model."""
    
    def test_memory_basic(self):
        """Test basic Memory creation."""
        memory = Memory(
            id="mem_123",
            session_id="session_456",
            content="Test memory content",
        )
        
        assert memory.id == "mem_123"
        assert memory.session_id == "session_456"
        assert memory.content == "Test memory content"
        assert isinstance(memory.timestamp, datetime)
    
    def test_memory_with_embedding(self):
        """Test Memory with embedding."""
        embedding = [0.1, 0.2, 0.3]
        memory = Memory(
            id="mem_123",
            session_id="session_456",
            content="Test content",
            embedding=embedding,
        )
        
        assert memory.embedding == embedding
    
    def test_memory_sensitive_flag(self):
        """Test Memory sensitive data flag."""
        memory = Memory(
            id="mem_123",
            session_id="session_456",
            content="Sensitive data",
            is_sensitive=True,
        )
        
        assert memory.is_sensitive is True


class TestUserProfile:
    """Test UserProfile model."""
    
    def test_user_profile_creation(self):
        """Test UserProfile creation."""
        profile = UserProfile(user_id="user_123")
        
        assert profile.user_id == "user_123"
        assert isinstance(profile.preferences, UserPreferences)
        assert isinstance(profile.created_at, datetime)
        assert isinstance(profile.updated_at, datetime)
    
    def test_user_profile_update_timestamp(self):
        """Test updating timestamp."""
        profile = UserProfile(user_id="user_123")
        original_time = profile.updated_at
        
        # Wait a tiny bit and update
        import time
        time.sleep(0.01)
        profile.update_timestamp()
        
        assert profile.updated_at > original_time
    
    def test_user_profile_with_preferences(self):
        """Test UserProfile with custom preferences."""
        prefs = UserPreferences(
            communication_style="formal",
            preferred_language="es",
        )
        
        profile = UserProfile(
            user_id="user_123",
            preferences=prefs,
        )
        
        assert profile.preferences.communication_style == "formal"
        assert profile.preferences.preferred_language == "es"


class TestTool:
    """Test Tool model."""
    
    def test_tool_creation(self):
        """Test Tool creation."""
        param_spec = ParameterSpec(
            name="query",
            type="string",
            description="Search query",
            required=True,
        )
        
        tool = Tool(
            name="search",
            description="Search tool",
            parameters={"query": param_spec},
        )
        
        assert tool.name == "search"
        assert "query" in tool.parameters
        assert tool.requires_auth is False
    
    def test_tool_with_auth(self):
        """Test Tool requiring authentication."""
        tool = Tool(
            name="api_call",
            description="API call tool",
            parameters={},
            requires_auth=True,
        )
        
        assert tool.requires_auth is True
