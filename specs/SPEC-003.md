# SPEC-003: Retrieval CLI

## Status
Complete

## Goal
Implement the "Agent Search" side of the system, allowing an orchestrator to query the vector database and receive JSON-formatted context.

## Requirements
1. Create a CLI command: `engram search <query> --limit <n>`.
2. Load the local embedding model to vectorize the incoming query.
3. Perform a similarity search against the LanceDB table created in SPEC-001.
4. Output results as a JSON array of objects, each containing:
   - `content`: The text chunk.
   - `source`: The file path.
   - `line`: The starting line number.
   - `score`: The distance/relevance score.

## Constraints
- Output must be valid JSON to allow for direct ingestion by agents via `exec`.
- Fail gracefully if the database has not been initialized.
