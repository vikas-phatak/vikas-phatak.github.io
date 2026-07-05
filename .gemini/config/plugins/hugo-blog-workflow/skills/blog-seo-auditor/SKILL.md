---
name: blog-seo-auditor
description: Audits blog post drafts for SEO optimization, readability scoring, OpenGraph cards, JSON-LD schema, and WCAG accessibility (a11y).
---

# Blog SEO & Accessibility Auditor Skill

Use this skill when auditing or reviewing draft articles before publishing to `vikasp.dev`.

## 1. SEO Checklist & Title Rules
- **Title Tag Length**: Keep article titles between **50 and 60 characters**. Titles over 65 characters risk being truncated in Google search results.
- **Meta Description**: Every post must include a `description` field in YAML frontmatter between **120 and 160 characters**. It must include primary technical keywords and a clear value proposition.
- **Heading Hierarchy**: Ensure strict `H1 -> H2 -> H3` heading structure. There should only be one `H1` (the post title rendered by the theme). In-article headings must start at `## H2`. Do not skip heading levels (e.g., jumping from `## H2` to `#### H4`).

## 2. OpenGraph (OG) & Twitter Cards
To maximize social sharing engagement on LinkedIn and X:
- Verify that a cover image (`cover.webp` or `cover.png`) exists in the page bundle.
- Ensure the frontmatter defines the `cover` attribute:
  ```yaml
  cover:
    image: "cover.webp"
    alt: "Architecture diagram showing multi-agent AI editorial workflow"
  ```
- The cover image should ideally be an aspect ratio of **16:9** (e.g., `1200x630` pixels).

## 3. JSON-LD Structured Data Schema
PaperMod automatically generates Schema.org JSON-LD metadata if frontmatter fields are properly populated. Verify:
- `author: "Vikas Phatak"` is explicitly defined.
- `date` is a valid ISO 8601 timestamp.
- `tags` and `categories` contain at least 2 relevant technical terms.

## 4. Accessibility (a11y) Quality Gate
Every image embedded in markdown (`![alt text](image.webp)`) MUST have descriptive `alt` text.
- **Bad**: `![image](chart.png)` or `![](chart.png)`
- **Good**: `![Bar chart comparing execution latency between plain python subprocess and uv run isolated sandboxes](chart.webp)`

## 5. Security & Secret Leak Check
Before signing off on any draft, scan the text and code snippets for accidental secret leaks:
- AWS keys (`AKIA...`)
- GitHub Personal Access Tokens (`ghp_...`, `github_pat_...`)
- OpenAI / LLM API keys (`sk-...`)
If any credential pattern is found, immediately reject the draft!
