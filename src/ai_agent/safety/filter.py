"""Safety filter."""

class SafetyFilter:
    """Filter harmful or inappropriate content."""
    
    def __init__(self):
        """Initialize safety filter."""
        self.blocked_patterns = ["harmful", "inappropriate", "offensive"]
    
    def filter_input(self, text: str) -> dict:
        """Filter input text."""
        for pattern in self.blocked_patterns:
            if pattern.lower() in text.lower():
                return {"blocked": True, "reason": f"Contains {pattern} content"}
        return {"blocked": False}
    
    def filter_output(self, text: str) -> dict:
        """Filter output text."""
        return self.filter_input(text)
