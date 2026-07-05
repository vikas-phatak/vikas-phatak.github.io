"""
Main CLI Orchestrator for the Autonomous Blog Workflow Management System.
"""
import typer
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel

from workflow.agents.researcher import ContentResearcher
from workflow.agents.writer import TechnicalWriter
from workflow.agents.editor import EditorInChief
from workflow.agents.verifier import CodeSnippetVerifier
from workflow.agents.syndicator import SocialSyndicator
from workflow.git_ops.publisher import GitPublisher

app = typer.Typer(
    name="blog-workflow",
    help="Autonomous Agent-Driven Hugo Blog Workflow Engine for vikasp.dev",
    add_completion=False
)
console = Console()

@app.command()
def new(
    topic: str = typer.Option(..., "--topic", "-t", help="Topic or title for the new blog post"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-g", help="Technical tags for the post"),
    auto_review: bool = typer.Option(True, "--auto-review/--no-review", help="Run editorial review immediately")
):
    """
    Bootstrap a clean Hugo post bundle using the AI Researcher and Writer agents.
    """
    console.print(Panel(f"[bold cyan]Initiating New Post Pipeline for:[/bold cyan] {topic}", expand=False))
    
    tag_list = tags if tags else ["Engineering", "AI"]
    
    # 1. Research phase
    researcher = ContentResearcher()
    res_result = researcher.run(topic=topic, tags=tag_list)
    if not res_result.success:
        console.print("[bold red]Research phase failed. Aborting pipeline.[/bold red]")
        raise typer.Exit(1)
        
    # 2. Writing phase
    writer = TechnicalWriter()
    write_result = writer.run(brief=res_result.output)
    if not write_result.success:
        console.print("[bold red]Writing phase failed. Aborting pipeline.[/bold red]")
        raise typer.Exit(1)
        
    post_dir = write_result.output["post_dir"]
    
    # 3. Editorial review phase (optional)
    if auto_review:
        editor = EditorInChief()
        edit_result = editor.run(post_dir=post_dir)
        if not edit_result.success:
            console.print("[bold yellow]Draft created but requires manual editorial adjustments.[/bold yellow]")
            raise typer.Exit(0)
            
    console.print(Panel(f"[bold green]Pipeline Complete![/bold green]\nPost bundle ready at: [cyan]{post_dir}[/cyan]", expand=False))

@app.command()
def review(
    post_dir: str = typer.Option(..., "--post-dir", "-d", help="Path to the Hugo post bundle directory")
):
    """
    Run Editor-in-Chief SEO, readability, and security audit on an existing draft.
    """
    console.print(Panel(f"[bold cyan]Running Editorial Audit on:[/bold cyan] {post_dir}", expand=False))
    editor = EditorInChief()
    res = editor.run(post_dir=post_dir)
    if not res.success:
        raise typer.Exit(1)
    console.print("[bold green]Review completed successfully![/bold green]")

@app.command()
def publish(
    post_dir: str = typer.Option(..., "--post-dir", "-d", help="Path to the approved Hugo post bundle directory"),
    title: str = typer.Option(..., "--title", "-t", help="Title of the post for Git commit and branch name"),
    auto_pr: bool = typer.Option(False, "--auto-pr", help="Automatically push branch and open GitHub PR via gh CLI")
):
    """
    Run Hugo pre-flight checks, create feature branch, commit, and open a GitHub Pull Request.
    """
    console.print(Panel(f"[bold cyan]Publishing Workflow Initiated for:[/bold cyan] {title}", expand=False))
    publisher = GitPublisher()
    res = publisher.run(post_dir=Path(post_dir), title=title, auto_pr=auto_pr)
    if not res.success:
        console.print(f"[bold red]Publishing failed:[/bold red] {res.errors}")
        raise typer.Exit(1)
    console.print("[bold green]Publishing sequence completed successfully![/bold green]")

@app.command()
def verify(
    post_dir: str = typer.Option(..., "--post-dir", "-d", help="Path to the Hugo post bundle directory")
):
    """
    Extract fenced markdown code snippets and execute them in sandboxed uv environments.
    """
    console.print(Panel(f"[bold cyan]Running Sandboxed Code Verification on:[/bold cyan] {post_dir}", expand=False))
    verifier = CodeSnippetVerifier()
    res = verifier.run(post_dir=post_dir)
    if not res.success:
        raise typer.Exit(1)

@app.command()
def syndicate(
    post_dir: str = typer.Option(..., "--post-dir", "-d", help="Path to the approved Hugo post bundle directory")
):
    """
    Generate promotional copy for LinkedIn, Twitter/X, and cross-posting developer blogs.
    """
    console.print(Panel(f"[bold cyan]Generating Social Syndication Copy for:[/bold cyan] {post_dir}", expand=False))
    syndicator = SocialSyndicator()
    res = syndicator.run(post_dir=post_dir)
    if not res.success:
        raise typer.Exit(1)

def cli():
    """Entry point for project script."""
    app()

if __name__ == "__main__":
    cli()
