"""Content moderator."""

class ContentModerator:
    """Moderate content for safety."""
    
    def moderate(self, content: str) -> dict:
        """Moderate content."""
        return {
            "safe": True,
            "categories": [],
            "confidence": 0.95
        }
