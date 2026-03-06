# Engram Skill

The Engram skill provides agents a way to query the local `engram` knowledge base, retrieve relevant indexed files, and stay informed of indexing freshness.

## Tooling
- `engram_query`: Searches the engram store. Returns matches along with freshness context.

## Prerequisites
- The `ENGRAM_STORE` environment variable MUST be set, pointing to the active `.lancedb` store directory.
- The project `main.py` is executed via `uv`.

## Process
1. Use `engram_query` with a search phrase. The wrapper will automatically format the query and search.
2. If `ENGRAM_STORE` is unset or invalid, the tool will return a friendly error. You must inform the human to set it.
3. If the result includes a message indicating new files exist and a reindex is needed, you MUST notify the user to run `uv run main.py index <path>`.

## Usage
The wrapper script handles the complexity:
```bash
./query.sh "what did I decide about LanceDB"
```
