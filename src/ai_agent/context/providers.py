"""Context providers."""

class StaticContextProvider:
    """Provide static reference material."""
    
    def __init__(self):
        """Initialize provider."""
        self.context = {}
    
    def get_context(self, domain: str) -> str:
        """Get static context for domain."""
        return self.context.get(domain, "")

class DynamicContextProvider:
    """Provide request-specific context."""
    
    def get_context(self, request_data: dict) -> str:
        """Generate dynamic context."""
        return f"Request context for: {request_data.get('message', '')}"
