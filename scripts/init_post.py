#!/usr/bin/env python3
"""
Quick utility script to bootstrap a clean post bundle without running full agent research.
"""
import sys
from pathlib import Path
from datetime import datetime, timezone
import yaml

ROOT_DIR = Path(__file__).parent.parent.resolve()
CONTENT_DIR = ROOT_DIR / "content" / "posts"

def init_post(title: str):
    slug = title.lower().strip().replace(" ", "-").replace("_", "-")
    post_dir = CONTENT_DIR / slug
    post_dir.mkdir(parents=True, exist_ok=True)
    index_file = post_dir / "index.md"
    
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    
    content = f"""---
title: "{title}"
date: {now_str}
author: "Vikas Phatak"
description: "Brief summary of {title}."
tags: ["Engineering"]
categories: ["Engineering"]
draft: true
ShowToc: true
---

## Introduction

Write your content here...
"""
    index_file.write_text(content, encoding="utf-8")
    print(f"Successfully bootstrapped post bundle at: {index_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/init_post.py <post-title>")
        sys.exit(1)
    init_post(sys.argv[1])
