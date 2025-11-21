"""Request orchestrator."""

from ..models import AgentRequest, AgentResponse

class RequestOrchestrator:
    """Orchestrate request processing."""
    
    def __init__(self):
        """Initialize orchestrator."""
        self.components = {}
    
    def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process agent request."""
        return AgentResponse(
            session_id=request.session_id,
            message=f"Processed: {request.message}",
            confidence=0.95
        )
