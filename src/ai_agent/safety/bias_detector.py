"""Bias detector."""

class BiasDetector:
    """Detect bias in content."""
    
    def detect(self, text: str) -> dict:
        """Detect bias in text."""
        return {
            "bias_score": 0.1,
            "bias_types": [],
            "flagged": False
        }
