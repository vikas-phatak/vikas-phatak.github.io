"""
Base Agent definitions for the multi-agent editorial board.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel
from rich.console import Console

console = Console()

class AgentResult(BaseModel):
    """Result returned by an agent execution."""
    agent_name: str
    success: bool
    output: Any
    errors: list[str] = []
    metadata: Dict[str, Any] = {}

class BaseAgent(ABC):
    """Abstract base class for all editorial board agents."""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    def log(self, message: str, style: str = "bold cyan"):
        """Log structured output to console."""
        console.print(f"[[bold green]{self.name}[/bold green]] ({self.role}): [{style}]{message}[/{style}]")

    @abstractmethod
    def run(self, *args, **kwargs) -> AgentResult:
        """Execute the agent's core task."""
        pass
