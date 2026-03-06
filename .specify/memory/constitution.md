<!--
Sync Impact Report:
- Version change: N/A → 1.0.0
- List of modified principles:
    - Principle 1: Local-First, Always
    - Principle 2: Performance as a Feature
    - Principle 3: Orchestration-Ready
    - Principle 4: Architect vs. Coder
    - Principle 5: Zero Hype
- Added sections: Vision, Strategic Direction
- Removed sections: None
- Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated/verified)
    - .specify/templates/spec-template.md (✅ updated/verified)
    - .specify/templates/tasks-template.md (✅ updated/verified)
- Follow-up TODOs: None
-->

# Engram Constitution

## Core Principles

### I. Local-First, Always
All embeddings and vector storage must reside on the host machine. No cloud dependencies for core retrieval. This ensures maximum privacy, offline availability, and eliminates external latency.

### II. Performance as a Feature
Use specialized tools like LanceDB and local embedding models to ensure sub-millisecond search results. Performance is not an afterthought but a core requirement for real-time agent interaction.

### III. Orchestration-Ready
Outputs must be machine-readable (JSON) and optimized for ingestion by LLM-based agents. Every component should be designed to be easily called and understood by an automated system.

### IV. Architect vs. Coder
The LLM acts as the Architect (the caller), while Engram acts as the high-speed Contractor (the executor). This clear separation of concerns ensures that the system remains deterministic, reliable, and focused on its core retrieval task.

### V. Zero Hype
Focus on reliable semantic retrieval and strict data validation rather than creative synthesis. Engram provides the facts; the agent provides the reasoning. Reliability and accuracy are prioritized over "smart" but unpredictable behavior.

## Vision
Engram is a high-performance, local-first "Memory Engine" designed to serve as an orchestration-ready retrieval layer for AI agents. It prioritizes speed, privacy, and deterministic integration over generative features.

## Strategic Direction
Engram will evolve from a simple directory indexer into a comprehensive local memory layer that supports multiple data sources, incremental updates, and complex metadata filtering.

## Governance
- Amendments to this constitution require a version bump and updated documentation.
- All implementation plans must include a "Constitution Check" to ensure alignment with these principles.
- Use `.specify/memory/constitution.md` as the source of truth for all governance decisions.
- Any deviation from these principles must be explicitly justified in the complexity tracking section of the implementation plan.

**Version**: 1.0.0 | **Ratified**: 2026-03-05 | **Last Amended**: 2026-03-05
