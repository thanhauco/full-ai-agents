"""Test configuration module."""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_env_file():
    """Create a temporary .env file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("TEST_VAR=test_value\n")
        f.write("LOG_LEVEL=DEBUG\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    test_vars = {
        "OPENAI_API_KEY": "test_openai_key",
        "ANTHROPIC_API_KEY": "test_anthropic_key",
        "LOG_LEVEL": "DEBUG",
        "API_HOST": "127.0.0.1",
        "API_PORT": "8000",
    }
    
    for key, value in test_vars.items():
        monkeypatch.setenv(key, value)
    
    return test_vars
