"""Unit tests for project setup and configuration."""

import logging
import os
from pathlib import Path

import pytest
import structlog

from config.logging_config import configure_logging, get_logger


class TestProjectSetup:
    """Test project structure and setup."""
    
    def test_project_structure_exists(self):
        """Test that required project directories exist."""
        required_dirs = ["src/ai_agent", "tests", "config", "docs"]
        
        for dir_path in required_dirs:
            assert Path(dir_path).exists(), f"Directory {dir_path} should exist"
            assert Path(dir_path).is_dir(), f"{dir_path} should be a directory"
    
    def test_init_files_exist(self):
        """Test that __init__.py files exist in Python packages."""
        init_files = [
            "src/ai_agent/__init__.py",
            "tests/__init__.py",
            "config/__init__.py",
        ]
        
        for init_file in init_files:
            assert Path(init_file).exists(), f"Init file {init_file} should exist"
    
    def test_env_example_exists(self):
        """Test that .env.example file exists."""
        assert Path(".env.example").exists(), ".env.example file should exist"
    
    def test_pyproject_toml_exists(self):
        """Test that pyproject.toml exists."""
        assert Path("pyproject.toml").exists(), "pyproject.toml should exist"


class TestLoggingConfiguration:
    """Test logging configuration."""
    
    def test_configure_logging_default_level(self):
        """Test that logging can be configured with default level."""
        configure_logging()
        
        # Verify structlog is configured
        logger = get_logger(__name__)
        assert logger is not None
        assert hasattr(logger, 'info')
        assert hasattr(logger, 'error')
        assert hasattr(logger, 'debug')
    
    def test_configure_logging_custom_level(self):
        """Test that logging can be configured with custom level."""
        configure_logging(log_level="DEBUG")
        
        logger = get_logger(__name__)
        assert logger is not None
    
    def test_configure_logging_various_levels(self):
        """Test that logging works with various log levels."""
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        for level in log_levels:
            configure_logging(log_level=level)
            logger = get_logger(__name__)
            assert logger is not None
    
    def test_get_logger_returns_structlog_instance(self):
        """Test that get_logger returns a structlog instance."""
        configure_logging()
        logger = get_logger("test_logger")
        
        assert logger is not None
        # Verify it has structlog methods
        assert hasattr(logger, 'bind')
        assert hasattr(logger, 'unbind')
    
    def test_logger_can_log_messages(self, caplog):
        """Test that logger can actually log messages."""
        configure_logging(log_level="INFO")
        logger = get_logger(__name__)
        
        # This should work without raising exceptions
        logger.info("test_message", key="value")
        logger.error("test_error", error_code=500)
    
    def test_logger_context_binding(self):
        """Test that logger can bind context."""
        configure_logging()
        logger = get_logger(__name__)
        
        # Bind context
        bound_logger = logger.bind(request_id="123", user_id="user_456")
        assert bound_logger is not None
        
        # Should be able to log with bound context
        bound_logger.info("test_with_context")


class TestConfigurationLoading:
    """Test configuration loading from environment."""
    
    def test_env_example_has_required_keys(self):
        """Test that .env.example contains required configuration keys."""
        required_keys = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "PINECONE_API_KEY",
            "LOG_LEVEL",
            "API_HOST",
            "API_PORT",
        ]
        
        with open(".env.example", "r") as f:
            content = f.read()
        
        for key in required_keys:
            assert key in content, f"Required key {key} should be in .env.example"
    
    def test_env_example_format(self):
        """Test that .env.example is properly formatted."""
        with open(".env.example", "r") as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            
            # Should be in KEY=value format
            assert "=" in line, f"Line should contain '=': {line}"
