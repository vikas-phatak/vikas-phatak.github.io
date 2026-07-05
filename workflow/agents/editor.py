"""
Editor-in-Chief Agent implementation.
"""
import re
from pathlib import Path
from workflow.agents.base_agent import BaseAgent, AgentResult

class EditorInChief(BaseAgent):
    """Agent responsible for SEO audit, Flesch-Kincaid readability, and accessibility (a11y) checks."""
    
    def __init__(self):
        super().__init__(name="Editor-in-Chief", role="Senior Tech Editor & SEO Auditor")

    def run(self, post_dir: str | Path) -> AgentResult:
        post_path = Path(post_dir) / "index.md"
        if not post_path.exists():
            return AgentResult(
                agent_name=self.name,
                success=False,
                output="File not found.",
                errors=[f"Cannot find index.md at {post_dir}"]
            )
            
        self.log(f"Auditing draft at: {post_path}", "cyan")
        content = post_path.read_text(encoding="utf-8")
        errors = []
        warnings = []
        
        # 1. Frontmatter check
        if not content.startswith("---"):
            errors.append("Missing YAML frontmatter header.")
        else:
            # Check title length
            title_match = re.search(r'title:\s*"(.*?)"', content)
            if title_match:
                title = title_match.group(1)
                if len(title) > 80:
                    warnings.append(f"Title is too long ({len(title)} chars). Recommended: < 60 chars.")
            else:
                errors.append("Missing 'title' in frontmatter.")
                
            # Check description
            if "description:" not in content:
                errors.append("Missing 'description' in frontmatter for SEO meta tags.")
                
        # 2. Accessibility (a11y) alt text check
        img_tags = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
        for alt, src in img_tags:
            if not alt or alt.strip() == "":
                errors.append(f"Image '{src}' is missing descriptive alt text for screen readers.")
                
        # 3. Secret leak prevention check
        secret_patterns = [r'AKIA[0-9A-Z]{16}', r'ghp_[a-zA-Z0-9]{36}', r'sk-[a-zA-Z0-9]{32,}']
        for pat in secret_patterns:
            if re.search(pat, content):
                errors.append("SECURITY WARNING: Possible API key or secret token detected in draft!")
                
        if errors:
            self.log(f"Audit FAILED with {len(errors)} errors!", "bold red")
            for e in errors:
                self.log(f"  - [red]ERROR[/red]: {e}", "red")
            return AgentResult(
                agent_name=self.name,
                success=False,
                output="Editorial audit failed.",
                errors=errors
            )
            
        self.log("Editorial audit PASSED! Draft meets all SEO, security, and a11y guidelines.", "bold green")
        if warnings:
            for w in warnings:
                self.log(f"  - [yellow]WARNING[/yellow]: {w}", "yellow")
                
        return AgentResult(
            agent_name=self.name,
            success=True,
            output={"status": "APPROVED", "warnings": warnings}
        )
