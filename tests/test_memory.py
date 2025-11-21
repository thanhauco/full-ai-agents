"""Tests for memory management."""

from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import pytest
from hypothesis import given, strategies as st

from src.ai_agent.models import Memory
from src.ai_agent.memory import MemoryManager, ShortTermMemory, LongTermMemory


class TestShortTermMemory:
    """Test short-term memory."""
    
    def test_add_and_retrieve(self):
        """Test adding and retrieving memories."""
        stm = ShortTermMemory()
        memory = Memory(id="1", session_id="s1", content="test")
        
        stm.add(memory)
        assert stm.size() == 1
        
        recent = stm.get_recent(1)
        assert len(recent) == 1
        assert recent[0].id == "1"
    
    def test_max_size(self):
        """Test max size limit."""
        stm = ShortTermMemory(max_size=3)
        
        for i in range(5):
            stm.add(Memory(id=str(i), session_id="s1", content=f"test{i}"))
        
        assert stm.size() == 3


class TestLongTermMemory:
    """Test long-term memory."""
    
    def test_store_and_retrieve(self):
        """Test storing and retrieving."""
        ltm = LongTermMemory()
        memory = Memory(id="1", session_id="s1", content="test")
        
        ltm.store(memory)
        retrieved = ltm.retrieve("1")
        
        assert retrieved is not None
        assert retrieved.id == "1"
    
    def test_encryption(self):
        """Test sensitive data encryption."""
        key = Fernet.generate_key()
        ltm = LongTermMemory(encryption_key=key)
        
        memory = Memory(id="1", session_id="s1", content="sensitive", is_sensitive=True)
        ltm.store(memory)
        
        # Content should be encrypted in storage
        stored = ltm.memories["1"]
        assert stored.content != "sensitive"
    
    def test_cleanup_old(self):
        """Test cleanup of old memories."""
        ltm = LongTermMemory()
        
        # Add old memory
        old_memory = Memory(id="1", session_id="s1", content="old")
        old_memory.timestamp = datetime.utcnow() - timedelta(days=40)
        ltm.store(old_memory)
        
        # Add recent memory
        new_memory = Memory(id="2", session_id="s1", content="new")
        ltm.store(new_memory)
        
        removed = ltm.cleanup_old(retention_days=30)
        assert removed == 1
        assert ltm.retrieve("2") is not None


class TestMemoryManager:
    """Test memory manager."""
    
    def test_store_interaction(self):
        """Test storing interaction."""
        manager = MemoryManager()
        memory = Memory(id="1", session_id="s1", content="test")
        
        manager.store_interaction(memory)
        
        assert manager.short_term.size() > 0
        assert manager.long_term.retrieve("1") is not None


# Property tests
class TestMemoryProperties:
    """Property-based tests for memory."""
    
    @given(
        content=st.text(min_size=1, max_size=100),
        session_id=st.text(min_size=1, max_size=50),
    )
    def test_short_term_memory_retrieval(self, content: str, session_id: str):
        """Property 15: Short-term memory retrieval."""
        stm = ShortTermMemory()
        memory = Memory(id="test", session_id=session_id, content=content)
        
        stm.add(memory)
        recent = stm.get_recent(1)
        
        assert len(recent) > 0
        assert recent[0].content == content
    
    @given(
        content=st.text(min_size=1, max_size=100),
    )
    def test_long_term_persistence(self, content: str):
        """Property 16: Long-term memory persistence."""
        ltm = LongTermMemory()
        memory = Memory(id="test", session_id="s1", content=content)
        
        ltm.store(memory)
        retrieved = ltm.retrieve("test")
        
        assert retrieved is not None
        assert retrieved.content == content
