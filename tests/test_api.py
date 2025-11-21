"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.ai_agent.api.app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    return TestClient(app)


class TestAPIEndpoints:
    """Test API endpoints."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_get_capabilities(self, client):
        """Test capabilities endpoint."""
        response = client.get("/capabilities")
        
        assert response.status_code == 200
        data = response.json()
        assert "capabilities" in data
        assert "models" in data
    
    def test_chat_endpoint(self, client):
        """Test chat endpoint."""
        response = client.post(
            "/chat",
            json={
                "message": "Hello",
                "session_id": "test_session",
                "user_id": "test_user",
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "session_id" in data
    
    def test_get_session(self, client):
        """Test get session endpoint."""
        response = client.get("/sessions/test_session")
        
        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test_session"
    
    def test_delete_session(self, client):
        """Test delete session endpoint."""
        response = client.delete("/sessions/test_session")
        
        assert response.status_code == 200
        data = response.json()
        assert data["deleted"] is True
