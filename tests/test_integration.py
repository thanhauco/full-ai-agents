"""Integration tests for the complete AI Agent system."""

import pytest
from fastapi.testclient import TestClient

from src.ai_agent.api.app import create_app
from src.ai_agent.models import AgentRequest, ModelConfig
from src.ai_agent.llm import TokenTracker
from src.ai_agent.memory import MemoryManager
from src.ai_agent.prompts import PromptManager
from src.ai_agent.orchestration import RequestOrchestrator, SessionManager
from src.ai_agent.monitoring import MetricsCollector, FeedbackCollector


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


class TestEndToEndIntegration:
    """End-to-end integration tests."""
    
    def test_complete_request_flow(self, client):
        """Test complete request flow through the system."""
        # Health check
        response = client.get("/health")
        assert response.status_code == 200
        
        # Get capabilities
        response = client.get("/capabilities")
        assert response.status_code == 200
        assert "capabilities" in response.json()
        
        # Send chat message
        response = client.post(
            "/chat",
            json={
                "message": "Hello, AI agent!",
                "session_id": "integration_test",
                "user_id": "test_user"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["session_id"] == "integration_test"
    
    def test_session_management_flow(self, client):
        """Test session management flow."""
        session_id = "test_session_123"
        
        # Create session by sending message
        response = client.post(
            "/chat",
            json={
                "message": "First message",
                "session_id": session_id,
                "user_id": "test_user"
            }
        )
        assert response.status_code == 200
        
        # Get session
        response = client.get(f"/sessions/{session_id}")
        assert response.status_code == 200
        
        # Delete session
        response = client.delete(f"/sessions/{session_id}")
        assert response.status_code == 200


class TestComponentIntegration:
    """Test integration between components."""
    
    def test_memory_and_orchestration(self):
        """Test memory manager with orchestration."""
        memory = MemoryManager()
        orchestrator = RequestOrchestrator()
        
        request = AgentRequest(
            session_id="test",
            user_id="user1",
            message="Test message"
        )
        
        response = orchestrator.process_request(request)
        assert response.session_id == "test"
    
    def test_prompt_and_token_tracking(self):
        """Test prompt manager with token tracking."""
        prompt_manager = PromptManager()
        token_tracker = TokenTracker()
        
        template = prompt_manager.get_template("default_agent")
        assert template is not None
        
        rendered = template.render(request="test request")
        assert "test request" in rendered
        
        # Track tokens
        token_tracker.record_usage(
            model="gpt-4",
            prompt_tokens=100,
            completion_tokens=50,
            cost=0.01
        )
        assert token_tracker.total_tokens == 150
    
    def test_monitoring_integration(self):
        """Test monitoring components."""
        metrics = MetricsCollector()
        feedback = FeedbackCollector()
        
        # Record metrics
        metrics.record_latency("test_operation", 0.5)
        assert len(metrics.get_metrics()) > 0
        
        # Record feedback
        feedback.record_feedback("session1", 5, "Great!")
        assert len(feedback.get_feedback()) > 0


class TestSystemResilience:
    """Test system resilience and error handling."""
    
    def test_invalid_request_handling(self, client):
        """Test handling of invalid requests."""
        # Missing required fields
        response = client.post("/chat", json={})
        assert response.status_code == 422  # Validation error
    
    def test_nonexistent_session(self, client):
        """Test handling of nonexistent session."""
        response = client.get("/sessions/nonexistent")
        assert response.status_code == 200  # Returns empty session
    
    def test_error_recovery(self):
        """Test error recovery mechanisms."""
        from src.ai_agent.orchestration import ErrorHandler
        
        handler = ErrorHandler()
        result = handler.handle_error(Exception("Test error"))
        
        assert "error" in result
        assert result["circuit_state"] in ["closed", "open"]


class TestPerformance:
    """Basic performance tests."""
    
    def test_concurrent_requests(self, client):
        """Test handling of concurrent requests."""
        import concurrent.futures
        
        def make_request():
            return client.post(
                "/chat",
                json={
                    "message": "Test",
                    "session_id": "perf_test",
                    "user_id": "user1"
                }
            )
        
        # Send 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [f.result() for f in futures]
        
        # All should succeed
        assert all(r.status_code == 200 for r in results)
    
    def test_response_time(self, client):
        """Test response time is reasonable."""
        import time
        
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 1.0  # Should respond in less than 1 second


class TestDataFlow:
    """Test data flow through the system."""
    
    def test_request_to_response_flow(self):
        """Test complete data flow from request to response."""
        from src.ai_agent.orchestration import RequestOrchestrator
        from src.ai_agent.models import AgentRequest
        
        orchestrator = RequestOrchestrator()
        
        request = AgentRequest(
            session_id="flow_test",
            user_id="user1",
            message="Test message",
            context={"key": "value"}
        )
        
        response = orchestrator.process_request(request)
        
        assert response.session_id == request.session_id
        assert response.message is not None
        assert response.confidence >= 0.0
        assert response.confidence <= 1.0


@pytest.mark.integration
class TestFullSystemIntegration:
    """Full system integration tests."""
    
    def test_all_components_initialized(self):
        """Test that all components can be initialized together."""
        from src.ai_agent.memory import MemoryManager
        from src.ai_agent.prompts import PromptManager
        from src.ai_agent.orchestration import RequestOrchestrator, SessionManager
        from src.ai_agent.monitoring import MetricsCollector, FeedbackCollector
        from src.ai_agent.context import ContextInjector
        from src.ai_agent.tools import ToolManager
        from src.ai_agent.safety import SafetyFilter
        from src.ai_agent.reasoning import ReasoningEngine
        
        # Initialize all components
        memory = MemoryManager()
        prompts = PromptManager()
        orchestrator = RequestOrchestrator()
        sessions = SessionManager()
        metrics = MetricsCollector()
        feedback = FeedbackCollector()
        context = ContextInjector()
        tools = ToolManager()
        safety = SafetyFilter()
        reasoning = ReasoningEngine()
        
        # Verify all initialized
        assert memory is not None
        assert prompts is not None
        assert orchestrator is not None
        assert sessions is not None
        assert metrics is not None
        assert feedback is not None
        assert context is not None
        assert tools is not None
        assert safety is not None
        assert reasoning is not None
    
    def test_system_health(self, client):
        """Test overall system health."""
        # Check health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        
        # Check capabilities
        response = client.get("/capabilities")
        assert response.status_code == 200
        capabilities = response.json()
        assert len(capabilities["capabilities"]) > 0
        assert len(capabilities["models"]) > 0
