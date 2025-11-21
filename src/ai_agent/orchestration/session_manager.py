"""Session manager."""

from typing import Dict, Any

class SessionManager:
    """Manage user sessions."""
    
    def __init__(self):
        """Initialize session manager."""
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, session_id: str) -> None:
        """Create a new session."""
        self.sessions[session_id] = {"messages": [], "created_at": None}
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session data."""
        return self.sessions.get(session_id, {})
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
