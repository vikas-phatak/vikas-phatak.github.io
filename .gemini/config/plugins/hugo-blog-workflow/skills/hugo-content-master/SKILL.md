---
name: hugo-content-master
description: Enforces Hugo static site conventions, page bundles, YAML frontmatter, shortcodes, and image optimization for vikas-phatak.github.io (vikasp.dev).
---

# Hugo Content Master Skill

Use this skill whenever drafting, reviewing, or structuring blog posts for `vikasp.dev`.

## 1. Page Bundle Structure
All blog posts MUST use Hugo Page Bundles. A page bundle is an isolated directory inside `content/posts/` containing the main markdown file (`index.md`) and all related assets (images, diagrams, data files).

```text
content/posts/my-post-slug/
├── index.md               # Main article content with YAML frontmatter
├── cover.webp             # OpenGraph and cover image (WebP format preferred)
└── architecture.svg       # Diagram or supplementary asset
```

## 2. Standard YAML Frontmatter
Always use YAML syntax (`---`) for frontmatter. Do not use TOML (`+++`) for article frontmatter.

### Required Frontmatter Schema:
```yaml
---
title: "Clear, descriptive title (50-60 characters)"
date: 2026-07-05T23:00:00+00:00
author: "Vikas Phatak"
description: "Compelling meta description summarizing the technical tutorial (120-160 characters)."
tags: ["AI", "Python", "Hugo"]
categories: ["Engineering", "AI Systems"]
draft: true
ShowToc: true
cover:
  image: "cover.webp"
  alt: "Descriptive alt text for accessibility"
  caption: "Image caption"
  relative: true
---
```

## 3. Shortcodes & Best Practices
- **Images**: Use standard Markdown or Hugo shortcodes. Always include descriptive `alt` text for screen readers.
  ```markdown
  ![Architecture Diagram of the Editorial Board](architecture.webp)
  ```
- **Internal Links**: Use Hugo `ref` or `relref` shortcodes to link to other posts to prevent dead links when slugs change:
  ```markdown
  See our [previous introduction]({{< ref "welcome-to-agentic-blog" >}}) for details.
  ```
- **Code Fences**: Always specify the language for syntax highlighting (`python`, `bash`, `yaml`, `json`).
  ```python
  def example():
      return "Monokai highlighted"
  ```

## 4. Image Processing & Optimization
- Prefer `WebP`, `AVIF`, or `SVG` formats over raw `PNG` or `JPEG`.
- Store images inside the page bundle directory (`content/posts/<slug>/`) so relative paths work cleanly across RSS feeds and OpenGraph cards.
