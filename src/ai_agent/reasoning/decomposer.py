"""Task decomposer."""

class TaskDecomposer:
    """Decompose complex tasks into steps."""
    
    def decompose(self, task: str) -> list:
        """Decompose task into steps."""
        return [
            {"step": 1, "action": "understand", "description": "Understand the task"},
            {"step": 2, "action": "plan", "description": "Plan the approach"},
            {"step": 3, "action": "execute", "description": "Execute the plan"}
        ]
