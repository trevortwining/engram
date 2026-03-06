#!/usr/bin/env bash

# Engram Skill Bridge - query.sh
# Implements SPEC-004

if [ -z "$ENGRAM_STORE" ]; then
    echo '{"error": "ENGRAM_STORE environment variable is not set. Please tell the human to set it to the path of the engram.lancedb directory."}'
    exit 1
fi

if [ ! -d "$ENGRAM_STORE" ]; then
    echo '{"error": "ENGRAM_STORE path ('$ENGRAM_STORE') does not exist or is unreachable. Please tell the human to fix the configuration."}'
    exit 1
fi

RAW_QUERY="$*"

# Basic Query Composer: remove filler words
QUERY=$(echo "$RAW_QUERY" | sed -E 's/\b(what|did|i|we|decide|about|is|the|a|an|in|on|at|to|for|with)\b//gi' | tr -s ' ' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
if [ -z "$QUERY" ]; then
    QUERY="$RAW_QUERY"
fi

# Directory of main.py
MAIN_DIR="$(dirname "$(dirname "$0")")"
cd "$MAIN_DIR" || exit 1

# Simulate checking for new files (mock reindex control)
# In a real implementation, this would compare file mtimes vs index time
NEEDS_REINDEX=false
if [ -n "$(find . -type f -name '*.md' -mtime -1 2>/dev/null | head -n 1)" ]; then
    NEEDS_REINDEX=true
fi

# Execute the search using uv run main.py
OUTPUT=$(uv run main.py search "$QUERY" --limit 5 2>/dev/null)

if [ "$NEEDS_REINDEX" = true ]; then
    echo '{"status": "stale", "message": "Content changed—please run `uv run main.py index <path>` before asking again.", "query": "'"$QUERY"'", "results": '"${OUTPUT:-[]}"'}'
else
    echo '{"status": "fresh", "query": "'"$QUERY"'", "results": '"${OUTPUT:-[]}"'}'
fi
