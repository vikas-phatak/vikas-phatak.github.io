#!/usr/bin/env bash
# Install uv and sync dependencies
echo "Setting up Python environment with uv..."
uv sync
echo "Environment setup complete! Run 'uv run blog-workflow --help' to get started."
