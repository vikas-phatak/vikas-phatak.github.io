---
name: social-syndication
description: Generates promotional copy for Twitter/X threads, LinkedIn professional announcements, and Markdown cross-posting payloads upon blog post approval.
---

# Social Syndication Skill

Use this skill once an article has passed all quality gates and has been submitted as a Pull Request or published to `vikasp.dev`.

## 1. LinkedIn Professional Announcement
Generate a clean, professional, and engaging post suitable for software engineers and engineering managers:
- **Hook**: Highlight a critical engineering challenge or architectural trade-off addressed in the post.
- **Body**: 3 bullet points summarizing the core takeaways or system benchmarks.
- **Call to Action (CTA)**: Provide the direct link to the published article (`https://vikasp.dev/posts/<slug>/`).
- **Hashtags**: Include 3-5 relevant hashtags (e.g., `#SoftwareEngineering`, `#AI`, `#Python`, `#SystemArchitecture`).

## 2. Twitter / X Thread (3-5 Tweets)
Create an engaging, fast-paced thread:
- **Tweet 1 (Hook)**: Contrasting statement or provocative insight with article link and cover image attached.
- **Tweet 2-3 (The Solution/Code)**: Share a concise insight or code pattern from the tutorial.
- **Final Tweet (Summary & Bookmark)**: Remind readers to bookmark and link back to the blog.

## 3. Cross-Posting Payload (Dev.to / Hashnode)
Generate canonical markdown for cross-posting to developer platforms:
- Ensure `canonical_url: https://vikasp.dev/posts/<slug>/` is included in the frontmatter so SEO juice flows back to the primary domain.
- Adjust image paths from relative page bundles to absolute URLs (`https://vikasp.dev/posts/<slug>/image.webp`).
