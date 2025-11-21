"""Token usage tracking for cost monitoring."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class TokenUsage:
    """Record of token usage."""
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    session_id: str = ""
    user_id: str = ""


class TokenTracker:
    """Track token usage across LLM calls."""
    
    def __init__(self):
        """Initialize token tracker."""
        self.usage_records: List[TokenUsage] = []
        self.total_tokens = 0
        self.total_cost = 0.0
    
    def record_usage(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float,
        session_id: str = "",
        user_id: str = "",
    ) -> None:
        """Record token usage.
        
        Args:
            model: Model name
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            cost: Cost in USD
            session_id: Session ID
            user_id: User ID
        """
        total_tokens = prompt_tokens + completion_tokens
        
        usage = TokenUsage(
            timestamp=datetime.utcnow(),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=cost,
            session_id=session_id,
            user_id=user_id,
        )
        
        self.usage_records.append(usage)
        self.total_tokens += total_tokens
        self.total_cost += cost
    
    def get_usage_by_session(self, session_id: str) -> List[TokenUsage]:
        """Get usage records for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            List of usage records
        """
        return [r for r in self.usage_records if r.session_id == session_id]
    
    def get_usage_by_user(self, user_id: str) -> List[TokenUsage]:
        """Get usage records for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of usage records
        """
        return [r for r in self.usage_records if r.user_id == user_id]
    
    def get_total_cost(self) -> float:
        """Get total cost across all usage.
        
        Returns:
            Total cost in USD
        """
        return self.total_cost
    
    def get_total_tokens(self) -> int:
        """Get total tokens across all usage.
        
        Returns:
            Total token count
        """
        return self.total_tokens
    
    def get_cost_by_model(self) -> Dict[str, float]:
        """Get cost breakdown by model.
        
        Returns:
            Dictionary mapping model names to costs
        """
        costs: Dict[str, float] = {}
        for record in self.usage_records:
            costs[record.model] = costs.get(record.model, 0.0) + record.cost
        return costs
