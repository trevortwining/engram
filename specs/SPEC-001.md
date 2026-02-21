# SPEC-001: Engram MVP (Minimum Viable Processor)

## Status
Complete

## Goal
Establish the core directory-to-vector pipeline using `uv`, `LanceDB`, and a local embedding model. This spec focuses solely on the "Index" half of the RAG equation.

## User Persona
An AI Agent (like TBot) that needs to programmatically index a directory of Markdown files to create a searchable memory.

## Core Features (Sub-Specs)
- **SPEC-002: Environment & Bootstrap:** Set up the `uv` project with dependencies (`lancedb`, `sentence-transformers`, `pyarrow`).
- **SPEC-003: Simple File Crawler:** A robust script to recursively find `.md` files in a given path.
- **SPEC-004: Local Embedding Pipeline:** Implementation of a `sentence-transformers` model (e.g., `all-MiniLM-L6-v2`) running on CPU.
- **SPEC-005: LanceDB Storage:** Schema definition and implementation for storing chunked text + embeddings + metadata (path, line number).

## Constraints
- **Format:** CLI-first.
- **Runtime:** Python 3.12+ (managed by `uv`).
- **Storage:** Local SQLite-backed LanceDB table.

## Success Criteria
- [ ] A user can run a command to index a directory.
- [ ] The resulting `engram.lancedb` folder is populated with vectorized data.
- [ ] Execution is performed entirely on the local CPU.
