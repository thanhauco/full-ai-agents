"""Comprehensive tests for all remaining components."""

import pytest
from hypothesis import given, strategies as st

from src.ai_agent.context import ContextInjector, StaticContextProvider, DynamicContextProvider, ContextFilter
from src.ai_agent.tools import ToolManager, ToolExecutor, ToolRegistry
from src.ai_agent.safety import SafetyFilter, ContentModerator, BiasDetector
from src.ai_agent.reasoning import ReasoningEngine, TaskDecomposer, StepExecutor
from src.ai_agent.orchestration import RequestOrchestrator, SessionManager, ErrorHandler
from src.ai_agent.monitoring import MetricsCollector, FeedbackCollector
from src.ai_agent.models import AgentRequest, Tool, ParameterSpec


class TestContextInjection:
    """Test context injection system."""
    
    def test_context_injector(self):
        """Test context injector."""
        injector = ContextInjector()
        request = AgentRequest(session_id="s1", user_id="u1", message="test")
        
        context = injector.inject_context(request)
        assert "static" in context
    
    def test_static_context_provider(self):
        """Test static context provider."""
        provider = StaticContextProvider()
        context = provider.get_context("domain")
        assert isinstance(context, str)
    
    def test_context_filter(self):
        """Test context filter."""
        filter = ContextFilter()
        filtered = filter.filter("test\nshort\nthis is a longer line")
        assert len(filtered) > 0


class TestToolManagement:
    """Test tool management system."""
    
    def test_tool_manager(self):
        """Test tool manager."""
        manager = ToolManager()
        tool = Tool(name="test", description="test tool", parameters={})
        
        manager.register_tool(tool)
        assert "test" in manager.list_tools()
    
    def test_tool_registry(self):
        """Test tool registry."""
        registry = ToolRegistry()
        tool = Tool(name="test", description="test tool", parameters={})
        
        registry.register(tool)
        assert registry.get("test") is not None


class TestSafetyFiltering:
    """Test safety filtering system."""
    
    def test_safety_filter(self):
        """Test safety filter."""
        filter = SafetyFilter()
        result = filter.filter_input("safe content")
        assert result["blocked"] is False
    
    def test_content_moderator(self):
        """Test content moderator."""
        moderator = ContentModerator()
        result = moderator.moderate("test content")
        assert "safe" in result
    
    def test_bias_detector(self):
        """Test bias detector."""
        detector = BiasDetector()
        result = detector.detect("test content")
        assert "bias_score" in result


class TestReasoningEngine:
    """Test reasoning engine."""
    
    def test_reasoning_engine(self):
        """Test reasoning engine."""
        engine = ReasoningEngine()
        steps = engine.reason("test query")
        assert len(steps) > 0
    
    def test_task_decomposer(self):
        """Test task decomposer."""
        decomposer = TaskDecomposer()
        steps = decomposer.decompose("complex task")
        assert len(steps) > 0


class TestOrchestration:
    """Test orchestration layer."""
    
    def test_request_orchestrator(self):
        """Test request orchestrator."""
        orchestrator = RequestOrchestrator()
        request = AgentRequest(session_id="s1", user_id="u1", message="test")
        
        response = orchestrator.process_request(request)
        assert response.session_id == "s1"
    
    def test_session_manager(self):
        """Test session manager."""
        manager = SessionManager()
        manager.create_session("s1")
        
        session = manager.get_session("s1")
        assert session is not None
    
    def test_error_handler(self):
        """Test error handler."""
        handler = ErrorHandler()
        result = handler.handle_error(Exception("test"))
        assert "error" in result


class TestMonitoring:
    """Test monitoring system."""
    
    def test_metrics_collector(self):
        """Test metrics collector."""
        collector = MetricsCollector()
        collector.record_latency("test_op", 0.5)
        
        metrics = collector.get_metrics()
        assert len(metrics) > 0
    
    def test_feedback_collector(self):
        """Test feedback collector."""
        collector = FeedbackCollector()
        collector.record_feedback("s1", 5, "great")
        
        feedback = collector.get_feedback()
        assert len(feedback) > 0


# Property-based tests
class TestComponentProperties:
    """Property-based tests for components."""
    
    @given(text=st.text(min_size=1, max_size=100))
    def test_safety_filter_property(self, text: str):
        """Property: Safety filter should always return a result."""
        filter = SafetyFilter()
        result = filter.filter_input(text)
        assert "blocked" in result
        assert isinstance(result["blocked"], bool)
    
    @given(session_id=st.text(min_size=1, max_size=50))
    def test_session_manager_property(self, session_id: str):
        """Property: Session manager should handle any session ID."""
        manager = SessionManager()
        manager.create_session(session_id)
        session = manager.get_session(session_id)
        assert session is not None
    
    @given(
        operation=st.text(min_size=1, max_size=50),
        duration=st.floats(min_value=0.0, max_value=100.0, allow_nan=False, allow_infinity=False)
    )
    def test_metrics_collector_property(self, operation: str, duration: float):
        """Property: Metrics collector should record any valid metric."""
        collector = MetricsCollector()
        collector.record_latency(operation, duration)
        metrics = collector.get_metrics()
        assert len(metrics) > 0
