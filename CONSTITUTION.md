# Engram Constitution

## Vision
Engram is a high-performance, local-first "Memory Engine" designed to serve as an orchestration-ready retrieval layer for AI agents. It prioritizes speed, privacy, and deterministic integration over generative features.

## Core Principles
1. **Local-First, Always:** All embeddings and vector storage must reside on the host machine. No cloud dependencies for core retrieval.
2. **Performance as a Feature:** Use specialized tools (e.g., LanceDB, local embedding models) to ensure sub-millisecond search results.
3. **Orchestration-Ready:** Outputs must be machine-readable (JSON) and optimized for ingestion by an LLM-based agent.
4. **Architect vs. Coder:** The LLM acts as the Architect (the caller), while Engram acts as the high-speed Contractor (the executor).
5. **Zero Hype:** Focus on reliable semantic retrieval and strict data validation rather than creative synthesis.

## Strategic Direction
Engram will evolve from a simple directory indexer into a comprehensive local memory layer that supports multiple data sources, incremental updates, and complex metadata filtering.
