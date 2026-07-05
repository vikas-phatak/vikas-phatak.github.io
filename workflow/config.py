"""
Configuration and system settings for the Blog Workflow Orchestration Engine.
"""
import os
from pathlib import Path
from pydantic import BaseModel, Field

# Base directories
ROOT_DIR = Path(__file__).parent.parent.resolve()
CONTENT_DIR = ROOT_DIR / "content" / "posts"
THEMES_DIR = ROOT_DIR / "themes"
SCRATCH_DIR = ROOT_DIR / "scratch"
TEMPLATES_DIR = ROOT_DIR / "workflow" / "templates"

# Ensure scratch directory exists
SCRATCH_DIR.mkdir(exist_ok=True)

class SystemConfig(BaseModel):
    """Global configuration for the agent workflow engine."""
    repo_owner: str = "vikas-phatak"
    repo_name: str = "vikas-phatak.github.io"
    default_branch: str = "main"
    hugo_theme: str = "PaperMod"
    base_url: str = "https://vikasp.dev/"
    
    # Execution timeouts
    verifier_timeout_seconds: int = 15
    use_isolated_uv_sandbox: bool = True
    
    # Quality Gates
    enforce_seo_audit: bool = True
    enforce_link_check: bool = True
    enforce_a11y_alt_text: bool = True

class PostFrontmatter(BaseModel):
    """Standardized schema for Hugo blog post frontmatter."""
    title: str = Field(..., description="SEO optimized title (50-60 characters recommended)")
    date: str = Field(..., description="ISO 8601 formatted date string")
    author: str = Field(default="Vikas Phatak")
    description: str = Field(..., description="Compelling meta description (120-160 characters)")
    tags: list[str] = Field(default_factory=list, description="List of technical tags")
    categories: list[str] = Field(default_factory=lambda: ["Engineering"], description="Top-level category")
    draft: bool = Field(default=True, description="Draft status")
    ShowToc: bool = Field(default=True, description="Enable Table of Contents")

CONFIG = SystemConfig()
