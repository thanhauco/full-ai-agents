"""Memory manager coordinating short and long-term memory."""

from typing import List, Optional

from ..models import Memory
from .short_term import ShortTermMemory
from .long_term import LongTermMemory


class MemoryManager:
    """Coordinate memory operations."""
    
    def __init__(self, encryption_key: Optional[bytes] = None):
        """Initialize memory manager.
        
        Args:
            encryption_key: Key for encrypting sensitive data
        """
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(encryption_key)
    
    def store_interaction(self, memory: Memory) -> None:
        """Store an interaction in both short and long-term memory.
        
        Args:
            memory: Memory to store
        """
        self.short_term.add(memory)
        self.long_term.store(memory)
    
    def retrieve_context(self, query_embedding: List[float], limit: int = 5) -> List[Memory]:
        """Retrieve relevant context.
        
        Args:
            query_embedding: Query embedding
            limit: Maximum results
            
        Returns:
            List of relevant memories
        """
        return self.long_term.search(query_embedding, limit)
    
    def get_conversation_history(self, session_id: str) -> List[Memory]:
        """Get conversation history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of memories for the session
        """
        return self.short_term.get_by_session(session_id)
    
    def cleanup_old_memories(self, retention_days: int = 30) -> int:
        """Clean up old memories.
        
        Args:
            retention_days: Days to retain
            
        Returns:
            Number of memories removed
        """
        return self.long_term.cleanup_old(retention_days)
