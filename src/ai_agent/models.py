"""Core data models for AI Agent System."""

from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class MultimodalInputType(str, Enum):
    """Types of multimodal inputs."""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"


class MultimodalInput(BaseModel):
    """Multimodal input data."""
    type: MultimodalInputType
    content: str  # URL, base64, or text content
    metadata: Optional[Dict[str, Any]] = None


class MultimodalOutput(BaseModel):
    """Multimodal output data."""
    type: MultimodalInputType
    content: str
    metadata: Optional[Dict[str, Any]] = None


class UserPreferences(BaseModel):
    """User preferences for personalization."""
    communication_style: Optional[str] = None
    preferred_language: str = "en"
    enable_voice: bool = False
    enable_images: bool = True
    custom_settings: Dict[str, Any] = Field(default_factory=dict)


class UserProfile(BaseModel):
    """User profile with preferences and settings."""
    user_id: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    interaction_history: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


class AgentRequest(BaseModel):
    """Request to the AI agent."""
    session_id: str
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None
    multimodal_inputs: Optional[List[MultimodalInput]] = None
    preferences: Optional[UserPreferences] = None
    
    @field_validator('message')
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        """Validate that message is not empty."""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v


class ReasoningStep(BaseModel):
    """A single step in multi-step reasoning."""
    step_number: int
    description: str
    action: str
    result: Any
    confidence: float = Field(ge=0.0, le=1.0)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ToolCall(BaseModel):
    """Record of a tool invocation."""
    tool_name: str
    parameters: Dict[str, Any]
    result: Any
    success: bool
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    duration_ms: Optional[float] = None


class AgentResponse(BaseModel):
    """Response from the AI agent."""
    session_id: str
    message: str
    reasoning_steps: List[ReasoningStep] = Field(default_factory=list)
    tool_calls: List[ToolCall] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    multimodal_outputs: Optional[List[MultimodalOutput]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Memory(BaseModel):
    """Memory entry for storage and retrieval."""
    id: str
    session_id: str
    content: str
    embedding: List[float] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    is_sensitive: bool = False


class ParameterSpec(BaseModel):
    """Specification for a tool parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None


class Tool(BaseModel):
    """Tool definition for external integrations."""
    name: str
    description: str
    parameters: Dict[str, ParameterSpec]
    requires_auth: bool = False
    
    class Config:
        arbitrary_types_allowed = True


class ModelConfig(BaseModel):
    """Configuration for LLM model."""
    provider: str = Field(default="openai", description="LLM provider (openai, anthropic)")
    model_name: str = Field(default="gpt-4", description="Model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, gt=0)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0)
    
    @field_validator('provider')
    @classmethod
    def validate_provider(cls, v: str) -> str:
        """Validate provider is supported."""
        supported = ["openai", "anthropic", "llama"]
        if v.lower() not in supported:
            raise ValueError(f"Provider must be one of {supported}")
        return v.lower()


class AgentConfig(BaseModel):
    """Configuration for the AI agent."""
    model_config: ModelConfig = Field(default_factory=ModelConfig)
    max_reasoning_steps: int = Field(default=10, gt=0)
    enable_tools: bool = True
    enable_memory: bool = True
    enable_safety_filter: bool = True
    cache_responses: bool = True
    parallel_tool_execution: bool = False
    memory_retention_days: int = Field(default=30, gt=0)
    max_context_length: int = Field(default=8000, gt=0)
