"""Long-term memory with vector storage."""

from datetime import datetime, timedelta
from typing import List, Optional
from cryptography.fernet import Fernet

from ..models import Memory


class LongTermMemory:
    """Persistent memory with vector database storage."""
    
    def __init__(self, encryption_key: Optional[bytes] = None):
        """Initialize long-term memory.
        
        Args:
            encryption_key: Key for encrypting sensitive data
        """
        self.memories: dict[str, Memory] = {}
        self.cipher = Fernet(encryption_key) if encryption_key else None
    
    def store(self, memory: Memory) -> None:
        """Store memory.
        
        Args:
            memory: Memory to store
        """
        # Encrypt sensitive data
        if memory.is_sensitive and self.cipher:
            memory.content = self.cipher.encrypt(memory.content.encode()).decode()
        
        self.memories[memory.id] = memory
    
    def retrieve(self, memory_id: str) -> Optional[Memory]:
        """Retrieve memory by ID.
        
        Args:
            memory_id: Memory ID
            
        Returns:
            Memory or None
        """
        memory = self.memories.get(memory_id)
        
        # Decrypt if needed
        if memory and memory.is_sensitive and self.cipher:
            memory.content = self.cipher.decrypt(memory.content.encode()).decode()
        
        return memory
    
    def search(self, query_embedding: List[float], limit: int = 10) -> List[Memory]:
        """Search memories by embedding similarity.
        
        Args:
            query_embedding: Query embedding vector
            limit: Maximum results
            
        Returns:
            List of similar memories
        """
        # Simple cosine similarity
        results = []
        for memory in self.memories.values():
            if memory.embedding:
                similarity = self._cosine_similarity(query_embedding, memory.embedding)
                results.append((similarity, memory))
        
        # Sort by similarity and return top results
        results.sort(reverse=True, key=lambda x: x[0])
        return [m for _, m in results[:limit]]
    
    def cleanup_old(self, retention_days: int = 30) -> int:
        """Remove old memories.
        
        Args:
            retention_days: Number of days to retain
            
        Returns:
            Number of memories removed
        """
        cutoff = datetime.utcnow() - timedelta(days=retention_days)
        to_remove = [
            mid for mid, mem in self.memories.items()
            if mem.timestamp < cutoff
        ]
        
        for mid in to_remove:
            del self.memories[mid]
        
        return len(to_remove)
    
    @staticmethod
    def _cosine_similarity(a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity.
        
        Args:
            a: First vector
            b: Second vector
            
        Returns:
            Similarity score
        """
        if len(a) != len(b):
            return 0.0
        
        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = sum(x * x for x in a) ** 0.5
        magnitude_b = sum(x * x for x in b) ** 0.5
        
        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0
        
        return dot_product / (magnitude_a * magnitude_b)
