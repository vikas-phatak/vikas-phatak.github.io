#!/usr/bin/env bash
# Launch Hugo dev server with draft preview enabled
echo "Starting local Hugo dev server at http://localhost:1313/"
hugo server -D --navigate-to-changed --panicOnWarning
