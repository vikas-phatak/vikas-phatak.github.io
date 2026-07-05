---
name: code-snippet-verifier
description: Extracts fenced code blocks from markdown tutorials and verifies them inside isolated uv sandboxes with inline PEP 723 dependencies.
---

# Code Snippet Verifier Skill

Use this skill to prevent link rot, broken syntax, or missing dependencies in code examples published on `vikasp.dev`.

## 1. Extraction Rules
When reviewing an article draft:
1. Scan the markdown for fenced code blocks (e.g., ` ```python `, ` ```bash `, ` ```js `).
2. Extract the code block content along with its language tag.
3. Ignore pseudo-code or configuration examples marked with `yaml`, `toml`, or `text`.

## 2. PEP 723 Inline Dependencies
For Python code snippets, check if external libraries are used (e.g., `pydantic`, `rich`, `langgraph`, `requests`, `numpy`, `pandas`, `typer`).
If dependencies are imported, ensure the snippet begins with PEP 723 inline script metadata:

```python
# /// script
# dependencies = ["pydantic>=2.7.0", "rich>=13.7.0"]
# ///
from pydantic import BaseModel
from rich import print
```

## 3. Sandboxed Execution via `uv`
To verify that code runs bug-free without polluting the host environment or failing due to missing packages:
1. Write the extracted snippet to a temporary scratch file in `scratch/test_snippet.py`.
2. Execute the script using `uv` in isolated mode with a strict timeout (e.g., 15 seconds):
   ```bash
   uv run --isolated scratch/test_snippet.py
   ```
3. If the command exits with code `0`, mark verification as **PASSED**.
4. If `stderr` contains tracebacks, syntax errors, or ModuleNotFoundError, mark as **FAILED**, capture the error log, and feed it back to the Technical Writer for correction.
