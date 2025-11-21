"""Context injector for enriching requests."""

from typing import Dict, Any
from ..models import AgentRequest

class ContextInjector:
    """Inject relevant context into agent requests."""
    
    def __init__(self):
        """Initialize context injector."""
        self.static_context: Dict[str, str] = {}
        self.session_context: Dict[str, list] = {}
    
    def inject_context(self, request: AgentRequest) -> Dict[str, Any]:
        """Inject context into request.
        
        Args:
            request: Agent request
            
        Returns:
            Enriched context dictionary
        """
        context = request.context or {}
        
        # Add static context
        context["static"] = self.static_context
        
        # Add session context
        if request.session_id in self.session_context:
            context["session_history"] = self.session_context[request.session_id]
        
        # Add user preferences
        if request.preferences:
            context["user_preferences"] = request.preferences.dict()
        
        return context
    
    def add_static_context(self, key: str, value: str) -> None:
        """Add static context."""
        self.static_context[key] = value
    
    def add_session_message(self, session_id: str, message: str) -> None:
        """Add message to session context."""
        if session_id not in self.session_context:
            self.session_context[session_id] = []
        self.session_context[session_id].append(message)
