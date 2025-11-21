"""Error handler with circuit breaker."""

import time

class ErrorHandler:
    """Handle errors with circuit breaker pattern."""
    
    def __init__(self):
        """Initialize error handler."""
        self.failure_count = 0
        self.failure_threshold = 5
        self.state = "closed"
    
    def handle_error(self, error: Exception) -> dict:
        """Handle an error."""
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
        
        return {
            "error": str(error),
            "circuit_state": self.state,
            "failure_count": self.failure_count
        }
