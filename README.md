# Engram (Local Memory Engine)
High-performance local retrieval for AI agents.

## Quick Start
1. Ensure `uv` is installed.
2. Install the tool locally:
   ```bash
   uv tool install .
   ```
3. Index your data:
   ```bash
   engram index ./docs
   ```
4. Search memory:
   ```bash
   engram search "how to use engram"
   ```

## Core Stack
- **Database:** LanceDB
- **Embeddings:** sentence-transformers (Local CPU)
- **Orchestrator:** TBot
