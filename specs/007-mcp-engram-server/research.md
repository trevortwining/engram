# Research: MCP Engram Server

## Unknown 1: Python MCP Server Implementation
- **Decision**: Use the official `mcp` package by Anthropic (`mcp[cli]`).
- **Rationale**: It is the standard, well-supported library for building Model Context Protocol servers in Python. It includes built-in support for `stdio` transport and easy decorators for defining tools.
- **Alternatives considered**: Writing a custom JSON-RPC implementation over stdin/stdout. Rejected because it adds unnecessary maintenance overhead and risks non-compliance with the rapidly evolving MCP specification.

## Unknown 2: LanceDB Lifecycle in an MCP Server
- **Decision**: Initialize the LanceDB connection upon server startup (using the MCP server lifecycle hooks or globally if simple) and keep it open for the duration of the stdio process.
- **Rationale**: The `stdio` transport implies a long-lived process per client connection. Initializing the DB once avoids the overhead of opening the LanceDB store on every search request, ensuring sub-millisecond search results (aligning with Constitution Principle II: Performance as a Feature).
- **Alternatives considered**: Opening and closing the database per tool call. Rejected due to performance overhead.

## Unknown 3: Handling Sentence-Transformers in MCP
- **Decision**: Load the local embedding model into memory when the server starts.
- **Rationale**: Similar to the database connection, model loading is slow. Loading it once keeps tool execution extremely fast (Constitution Principle I & II).

## Unknown 4: Exposing the Server CLI
- **Decision**: Add a new Typer command `engram mcp` or expose a dedicated entrypoint script that runs the `mcp` stdio server.
- **Rationale**: Fits well into the existing `typer` CLI structure defined in `pyproject.toml`.
- **Alternatives considered**: Creating a separate package. Rejected because it's tightly coupled with the core engram logic and data structures.
