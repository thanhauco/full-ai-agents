"""Metrics collector."""

from datetime import datetime
from typing import Dict, List

class MetricsCollector:
    """Collect performance metrics."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: List[Dict] = []
    
    def record_latency(self, operation: str, duration: float) -> None:
        """Record latency metric."""
        self.metrics.append({
            "type": "latency",
            "operation": operation,
            "duration": duration,
            "timestamp": datetime.utcnow()
        })
    
    def record_error(self, error: Exception, context: Dict) -> None:
        """Record error."""
        self.metrics.append({
            "type": "error",
            "error": str(error),
            "context": context,
            "timestamp": datetime.utcnow()
        })
    
    def get_metrics(self) -> List[Dict]:
        """Get all metrics."""
        return self.metrics
