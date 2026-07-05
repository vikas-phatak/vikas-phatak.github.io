"""
Code Snippet Verifier Agent - Extracts fenced markdown code blocks and verifies them
inside isolated sandboxes using uv run --isolated.
"""
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any, List
from rich.panel import Panel

from workflow.agents.base_agent import BaseAgent, AgentResult

class CodeSnippetVerifier(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Code Snippet Verifier",
            role="Sandboxed Execution & Syntax QA Engineer"
        )

    def run(self, post_dir: str | Path, **kwargs) -> AgentResult:
        post_path = Path(post_dir) / "index.md"
        if not post_path.exists():
            return AgentResult(
                success=False,
                output={},
                errors=[f"Article not found at: {post_path}"]
            )

        self.log(f"Scanning for fenced code snippets in: {post_path}")
        content = post_path.read_text(encoding="utf-8")
        
        # Parse fenced code blocks: ```python ... ``` or ```bash ... ```
        pattern = re.compile(r"```(python|py|bash|sh)\n(.*?)```", re.DOTALL)
        matches = pattern.findall(content)

        if not matches:
            self.log("No executable Python or Bash snippets found in article.")
            return AgentResult(
                success=True,
                output={"verified_count": 0, "results": []},
                errors=[]
            )

        self.log(f"Found {len(matches)} executable code block(s). Running sandbox verification...")
        
        results = []
        all_passed = True
        errors = []

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            for idx, (lang, code_text) in enumerate(matches, 1):
                lang_clean = lang.lower()
                if lang_clean in ("python", "py"):
                    script_file = temp_path / f"snippet_{idx}.py"
                    script_file.write_text(code_text, encoding="utf-8")
                    
                    self.log(f"Executing Python snippet #{idx} via 'uv run --isolated'...")
                    cmd = ["uv", "run", "--isolated", str(script_file)]
                elif lang_clean in ("bash", "sh"):
                    script_file = temp_path / f"snippet_{idx}.sh"
                    script_file.write_text(code_text, encoding="utf-8")
                    
                    self.log(f"Executing Bash snippet #{idx} via subprocess...")
                    cmd = ["bash", str(script_file)]
                else:
                    continue

                try:
                    proc = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=15
                    )
                    if proc.returncode == 0:
                        self.log(f"[green]Snippet #{idx} ({lang_clean}) PASSED![/green]")
                        results.append({
                            "id": idx,
                            "lang": lang_clean,
                            "status": "PASSED",
                            "stdout": proc.stdout.strip()
                        })
                    else:
                        all_passed = False
                        err_msg = f"Snippet #{idx} ({lang_clean}) FAILED (exit code {proc.returncode}):\n{proc.stderr.strip()}"
                        self.log(f"[red]{err_msg}[/red]")
                        errors.append(err_msg)
                        results.append({
                            "id": idx,
                            "lang": lang_clean,
                            "status": "FAILED",
                            "stderr": proc.stderr.strip()
                        })
                except subprocess.TimeoutExpired:
                    all_passed = False
                    err_msg = f"Snippet #{idx} ({lang_clean}) FAILED due to execution TIMEOUT (15s limit exceeded)."
                    self.log(f"[red]{err_msg}[/red]")
                    errors.append(err_msg)
                    results.append({
                        "id": idx,
                        "lang": lang_clean,
                        "status": "TIMEOUT",
                        "stderr": "Execution timed out after 15 seconds."
                    })

        if all_passed:
            self.console.print(Panel("[bold green]All Code Snippets Verified Successfully![/bold green]\nNo syntax errors or dependency failures detected.", expand=False))
            return AgentResult(
                success=True,
                output={"verified_count": len(matches), "results": results},
                errors=[]
            )
        else:
            self.console.print(Panel(f"[bold red]Code Verification Failed![/bold red]\n{len(errors)} snippet(s) encountered runtime or syntax errors.", expand=False))
            return AgentResult(
                success=False,
                output={"verified_count": len(matches), "results": results},
                errors=errors
            )
