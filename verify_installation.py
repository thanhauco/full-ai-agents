#!/usr/bin/env python3
"""Verification script to check installation and basic functionality."""

import sys
from pathlib import Path


def check_imports():
    """Check that all core modules can be imported."""
    print("Checking imports...")
    
    try:
        from src.ai_agent import models, config
        from src.ai_agent.llm import OpenAIProvider, AnthropicProvider, TokenTracker
        from src.ai_agent.memory import MemoryManager, ShortTermMemory, LongTermMemory
        from src.ai_agent.prompts import PromptTemplate, PromptManager, PromptRenderer
        from src.ai_agent.api import create_app
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def check_structure():
    """Check that required directories and files exist."""
    print("\nChecking project structure...")
    
    required_paths = [
        "src/ai_agent",
        "tests",
        "config",
        "docs",
        ".env.example",
        "pyproject.toml",
        "Dockerfile",
        "docker-compose.yml",
        "README.md",
    ]
    
    all_exist = True
    for path in required_paths:
        if Path(path).exists():
            print(f"✅ {path}")
        else:
            print(f"❌ {path} not found")
            all_exist = False
    
    return all_exist


def check_models():
    """Check that models can be instantiated."""
    print("\nChecking data models...")
    
    try:
        from src.ai_agent.models import (
            ModelConfig,
            AgentConfig,
            AgentRequest,
            AgentResponse,
            Memory,
        )
        
        # Test model creation
        config = ModelConfig(provider="openai")
        agent_config = AgentConfig()
        request = AgentRequest(
            session_id="test",
            user_id="test",
            message="test"
        )
        
        print("✅ All models can be instantiated")
        return True
    except Exception as e:
        print(f"❌ Model error: {e}")
        return False


def check_api():
    """Check that API can be created."""
    print("\nChecking API...")
    
    try:
        from src.ai_agent.api import create_app
        
        app = create_app()
        print("✅ API application created successfully")
        return True
    except Exception as e:
        print(f"❌ API error: {e}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("AI Agent System - Installation Verification")
    print("=" * 60)
    
    checks = [
        check_structure(),
        check_imports(),
        check_models(),
        check_api(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("✅ All checks passed! Installation is complete.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and add your API keys")
        print("2. Run: poetry run uvicorn src.ai_agent.api.app:create_app --factory --reload")
        print("3. Visit: http://localhost:8000/health")
        print("=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
