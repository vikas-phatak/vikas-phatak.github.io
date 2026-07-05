"""
Social Syndication Agent - Automatically generates promotional copy for LinkedIn,
Twitter/X, and developer cross-posting platforms.
"""
from pathlib import Path
from typing import Dict, Any
import yaml
from rich.panel import Panel

from workflow.agents.base_agent import BaseAgent, AgentResult

class SocialSyndicator(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Social Syndicator",
            role="Technical Evangelist & Brand Copywriter"
        )

    def run(self, post_dir: str | Path, **kwargs) -> AgentResult:
        post_path = Path(post_dir)
        index_file = post_path / "index.md"
        if not index_file.exists():
            return AgentResult(
                success=False,
                output={},
                errors=[f"Article not found at: {index_file}"]
            )

        self.log(f"Extracting frontmatter and content from: {index_file}")
        content = index_file.read_text(encoding="utf-8")
        
        # Parse YAML frontmatter
        title = "Untitled Post"
        description = "Check out our latest engineering blog post."
        tags = ["Engineering", "AI"]
        slug = post_path.name

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    fm = yaml.safe_load(parts[1])
                    if isinstance(fm, dict):
                        title = fm.get("title", title)
                        description = fm.get("description", description)
                        tags = fm.get("tags", tags)
                except Exception as e:
                    self.log(f"[yellow]Warning: Frontmatter parsing error: {e}[/yellow]")

        url = f"https://vikasp.dev/posts/{slug}/"
        hashtags_str = " ".join([f"#{t.replace(' ', '')}" for t in tags[:4]])

        self.log("Synthesizing multi-channel promotional copy...")

        # 1. LinkedIn Announcement
        linkedin_copy = f"""🚀 New Technical Article Published on vikasp.dev!

{title}

💡 Summary:
{description}

Key Takeaways:
• Architectural patterns and design trade-offs explored in depth.
• Complete, sandboxed code examples you can run locally.
• Performance benchmarks and system optimization guidelines.

🔗 Read the full post here: {url}

{hashtags_str} #SoftwareEngineering #TechBlog"""

        # 2. Twitter / X Thread
        twitter_thread = [
            f"1/ 🧵 Just published a deep-dive tutorial on vikasp.dev:\n\n{title}\n\n{description}\n\n🔗 {url}\n\n{hashtags_str}",
            f"2/ Why is this important?\n\nModern engineering requires combining autonomous AI agents with strict quality gates and reproducible environments.\n\nHere is how we structured the system to guarantee zero link rot and clean sandboxed execution 👇",
            f"3/ All code examples in this post were automatically tested and verified inside isolated @uv Python sandboxes before publishing.\n\nCheck out the full walkthrough and code snippets:\n{url}"
        ]

        # 3. Cross-posting Markdown Payload
        crosspost_copy = f"""---
title: "{title}"
published: true
tags: {tags[:4]}
canonical_url: "{url}"
---

*This article was originally published on [vikasp.dev]({url}).*

---

{description}

*(Read the full interactive tutorial and view source diagrams at [{url}]({url}))*
"""

        syndication_bundle = {
            "url": url,
            "linkedin": linkedin_copy,
            "twitter_thread": twitter_thread,
            "crosspost_payload": crosspost_copy
        }

        # Write promotional copy to an asset file inside the post bundle
        promo_file = post_path / "syndication_copy.md"
        promo_md = f"""# Social Syndication Copy for: {title}
Canonical URL: {url}

---

## 💼 LinkedIn Announcement
```text
{linkedin_copy}
```

---

## 🐦 Twitter / X Thread
```text
{twitter_thread[0]}

---

{twitter_thread[1]}

---

{twitter_thread[2]}
```

---

## 🌐 Dev.to / Hashnode Cross-post Frontmatter
```yaml
{crosspost_copy}
```
"""
        promo_file.write_text(promo_md, encoding="utf-8")
        self.log(f"[green]Syndication package saved to:[/green] {promo_file}")

        self.console.print(Panel(f"[bold green]Social Copy Generated![/bold green]\nPromotional package saved at: [cyan]{promo_file}[/cyan]", expand=False))
        return AgentResult(
            success=True,
            output=syndication_bundle,
            errors=[]
        )
