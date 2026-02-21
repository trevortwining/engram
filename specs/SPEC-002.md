# SPEC-002: Environment & Bootstrap

## Status
Complete

## Goal
Initialize the `engram` project using `uv` and configure the necessary dependencies for a local vector-search environment.

## Requirements
1. Initialize a new `uv` project in `~/projects/utils/engram`.
2. Add dependencies:
   - `lancedb` (Vector storage)
   - `sentence-transformers` (Local embeddings)
   - `pyarrow` (Required for LanceDB/data handling)
   - `click` or `typer` (CLI structure)
   - `pytest` (Testing)
3. Configure a `.env` file for local path defaults (e.g., `ENGRAM_DB_PATH`).

## Testing Requirements
- [ ] `uv run python --version` returns 3.12+.
- [ ] Dependencies can be imported in a python shell without error.
