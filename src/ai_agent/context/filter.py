"""Context filtering."""

class ContextFilter:
    """Filter irrelevant information from context."""
    
    def filter(self, context: str, relevance_threshold: float = 0.5) -> str:
        """Filter context by relevance."""
        # Simple implementation - remove very short or empty lines
        lines = context.split('\n')
        filtered = [line for line in lines if len(line.strip()) > 10]
        return '\n'.join(filtered)
