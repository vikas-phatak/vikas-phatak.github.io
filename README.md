# Autonomous Agent-Driven Blog Workflow Management System
**Repository**: `vikas-phatak/vikas-phatak.github.io`  
**Platform**: GitHub Pages + Hugo (PaperMod) + Python Agent Orchestration Engine

---

## 🌟 Overview

This repository hosts both the live Hugo static dev blog (`vikasp.dev`) and the backend **Autonomous Multi-Agent Editorial Board** described in [`vikas-phatak-personal-blog-wf-proposal.md`](file:///D:/Projects/vikas-phatak.github.io/vikas-phatak-personal-blog-wf-proposal.md).

## 🛠️ Architecture & Core Components

1. **Static Site Generator**: [Hugo](https://gohugo.io/) configured with [PaperMod](https://github.com/adityatelange/hugo-PaperMod).
2. **Orchestration Engine**: Python 3.10+ CLI managed by `uv` with sandboxed PEP 723 code execution.
3. **Multi-Agent Editorial Pipeline**: Specialized agents taking roles from ideation to code verification and git publishing.
4. **CI/CD Quality Gates**: Automated GitHub Actions (`.github/workflows/deploy-hugo.yml`) for zero-touch deployment with link checking (`lychee`).

---

## 🚀 Getting Started

### 1. Run Local Dev Server (Hugo)
Ensure Hugo Extended is installed, then launch the local preview server:
```bash
hugo server -D --navigate-to-changed
```
Open `http://localhost:1313/` in your browser.

### 2. Python Orchestration Engine
We use `uv` for ultra-fast Python dependency management:
```bash
# Sync dependencies
uv sync

# Run orchestrator CLI (coming in Phase 2)
uv run blog-workflow --help
```

---

## 📅 Roadmap & Progress

- [x] **Phase 1: Repository & Hugo Bootstrap**
  - [x] Configure `hugo.toml` with PaperMod theme and SEO defaults.
  - [x] Create initial page bundle in `content/posts/welcome-to-engineering-dispatches/`.
  - [x] Set up `.github/workflows/deploy-hugo.yml` with `lychee` link checker.
  - [x] Initialize Python `pyproject.toml` and `uv.lock`.
- [x] **Phase 2: Core Orchestration Engine & Existing Skills**
  - [x] Build `workflow/orchestrator.py` and CLI commands (`new`, `review`, `publish`).
  - [x] Implement `workflow/git_ops/publisher.py`.
- [x] **Phase 3: Custom Hugo & Editorial Skills Development**
  - [x] Build Antigravity Plugin `.gemini/config/plugins/hugo-blog-workflow/`.
  - [x] Implement `hugo-content-master` and `blog-seo-auditor` skills.
- [ ] **Phase 4: Advanced Code Verification & Social Syndication**
  - [ ] Implement `workflow/agents/verifier.py` using `uv run --isolated` with inline PEP 723 dependencies.
  - [ ] Add GitHub PR Review Feedback Loop webhook.
