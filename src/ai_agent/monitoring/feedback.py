"""Feedback collector."""

from datetime import datetime
from typing import List, Dict

class FeedbackCollector:
    """Collect user feedback."""
    
    def __init__(self):
        """Initialize feedback collector."""
        self.feedback: List[Dict] = []
    
    def record_feedback(self, session_id: str, rating: int, comment: str = "") -> None:
        """Record user feedback."""
        self.feedback.append({
            "session_id": session_id,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.utcnow()
        })
    
    def get_feedback(self, session_id: str = None) -> List[Dict]:
        """Get feedback."""
        if session_id:
            return [f for f in self.feedback if f["session_id"] == session_id]
        return self.feedback
