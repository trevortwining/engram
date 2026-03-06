# Implementation Plan: `engram` CLI Command

**Branch**: `006-engram-cli-command` | **Date**: 2026-03-05 | **Spec**: [specs/006-engram-cli-command/spec.md](specs/006-engram-cli-command/spec.md)
**Input**: Feature specification from `/specs/006-engram-cli-command/spec.md`

## Summary
The goal is to transition the Engram tool from being run via `uv run main.py` to a globally available `engram` command on the local machine. This will be achieved by moving to a standard `src/` layout, defining a `[project.scripts]` entry point in `pyproject.toml`, and using `uv tool install` for installation.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: `lancedb`, `pyarrow`, `sentence-transformers`, `typer`  
**Storage**: LanceDB (Local)  
**Testing**: pytest  
**Target Platform**: Local user machine (Linux/macOS/Windows)  
**Project Type**: CLI tool  
**Performance Goals**: N/A (parity with current)  
**Constraints**: Must use `uv` for dependency and environment management.  
**Scale/Scope**: Single local machine usage.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Local-First, Always**: ✅ The tool remains entirely local.
- **Performance as a Feature**: ✅ Use of LanceDB is maintained.
- **Orchestration-Ready**: ✅ The `engram` command simplifies agent orchestration.
- **Architect vs. Coder**: ✅ Engram remains the executor (Contractor).
- **Zero Hype**: ✅ Focus is on reliable retrieval.

## Project Structure

### Documentation (this feature)

```text
specs/006-engram-cli-command/
├── plan.md              # This file
├── research.md          # Packaging and installation research
├── data-model.md        # Distribution and installation flow
├── quickstart.md        # User installation guide
├── contracts/
│   └── cli-schema.md    # CLI command and output schema
└── tasks.md             # Implementation tasks
```

### Source Code (repository root)

```text
src/
└── engram/
    ├── __init__.py
    └── main.py          # Moved from root, updated with main()
pyproject.toml           # Updated with [project.scripts]
```

**Structure Decision**: Standard `src/` layout (Option 1). This is the most reliable way to handle console scripts in modern Python packaging.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       |            |                                     |
