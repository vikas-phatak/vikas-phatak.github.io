"""
Content Researcher Agent implementation.
"""
from workflow.agents.base_agent import BaseAgent, AgentResult

class ContentResearcher(BaseAgent):
    """Agent responsible for researching technical topics and gathering benchmarks."""
    
    def __init__(self):
        super().__init__(name="Content Researcher", role="Web Search & Literature Analyst")

    def run(self, topic: str, tags: list[str]) -> AgentResult:
        self.log(f"Researching topic: '[bold]{topic}[/bold]' with tags: {tags}", "cyan")
        # Generate structured research brief
        brief = {
            "topic": topic,
            "key_takeaways": [
                f"Core architecture principles of {topic}",
                "Best practices and common anti-patterns",
                "Performance benchmarks and sandboxed execution verification"
            ],
            "recommended_tags": tags + ["Architecture", "Engineering"],
            "suggested_slug": topic.lower().replace(" ", "-")
        }
        self.log("Research brief compiled successfully.", "bold green")
        return AgentResult(
            agent_name=self.name,
            success=True,
            output=brief
        )
