"""Short-term memory implementation."""

from collections import deque
from typing import List, Optional

from ..models import Memory


class ShortTermMemory:
    """In-memory buffer for active conversation context."""
    
    def __init__(self, max_size: int = 100):
        """Initialize short-term memory.
        
        Args:
            max_size: Maximum number of memories to store
        """
        self.max_size = max_size
        self.memories: deque = deque(maxlen=max_size)
    
    def add(self, memory: Memory) -> None:
        """Add memory to buffer.
        
        Args:
            memory: Memory to add
        """
        self.memories.append(memory)
    
    def get_recent(self, limit: int = 10) -> List[Memory]:
        """Get recent memories.
        
        Args:
            limit: Number of memories to retrieve
            
        Returns:
            List of recent memories
        """
        return list(self.memories)[-limit:]
    
    def get_by_session(self, session_id: str) -> List[Memory]:
        """Get memories for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of memories for the session
        """
        return [m for m in self.memories if m.session_id == session_id]
    
    def clear(self) -> None:
        """Clear all memories."""
        self.memories.clear()
    
    def size(self) -> int:
        """Get current size.
        
        Returns:
            Number of memories stored
        """
        return len(self.memories)
