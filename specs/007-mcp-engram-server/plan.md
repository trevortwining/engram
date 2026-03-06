# Implementation Plan: MCP Engram Server

**Branch**: `001-mcp-engram-server` | **Date**: 2026-03-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-mcp-engram-server/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Implement a Model Context Protocol (MCP) server for Engram using the Anthropic `mcp` Python package. The server will use the `stdio` transport to expose a `search_engram` tool, allowing AI assistants like Cursor and Claude to semantically query the local LanceDB store for context.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: `mcp`, `lancedb`, `sentence-transformers`, `typer`
**Storage**: Local LanceDB (`engram.lancedb/`)
**Testing**: `pytest`
**Target Platform**: Any OS supporting the Python MCP SDK
**Project Type**: CLI tool extension (MCP Server)
**Performance Goals**: <1s response time for search queries
**Constraints**: Local-first only, must not use cloud embeddings or search
**Scale/Scope**: Single local user database, typical size < 1GB

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Local-First, Always**: Search relies strictly on the local LanceDB store and local `sentence-transformers` model. No cloud dependency is introduced.
- [x] **II. Performance as a Feature**: Connections to LanceDB and embedding models are held in memory during the long-lived MCP `stdio` session for sub-millisecond querying.
- [x] **III. Orchestration-Ready**: Exposes a standard MCP tool (`search_engram`) returning deterministic text structures with metadata, built specifically for agent consumption.
- [x] **IV. Architect vs. Coder**: Engram continues to serve as the retrieval layer; no reasoning or LLM generation is added to the server logic.
- [x] **V. Zero Hype**: Implements only standard semantic search using existing tools; no speculative features.

## Project Structure

### Documentation (this feature)

```text
specs/001-mcp-engram-server/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── mcp-tool-schema.md
└── tasks.md             # Phase 2 output (future)
```

### Source Code (repository root)

```text
src/
└── engram/
    ├── __init__.py
    ├── main.py          # Updated with `mcp` command
    └── mcp/             # New module for MCP server logic
        ├── __init__.py
        ├── server.py    # MCP stdio server definition
        └── tools.py     # search_engram tool logic

tests/
├── test_bridge.py
├── test_engram.py
└── test_mcp.py          # New tests for MCP endpoints
```

**Structure Decision**: Kept within the main `engram` package as a submodule `engram.mcp`, with the CLI entrypoint added to `engram.main`. This aligns with existing structure and minimizes package fragmentation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |
