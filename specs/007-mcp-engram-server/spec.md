# Feature Specification: MCP Engram Server

**Feature Branch**: `001-mcp-engram-server`  
**Created**: Friday, March 6, 2026  
**Status**: Draft  
**Input**: User description: "Create a new feature for a basic MCP tool for engram. It should allow searches and results of the engram store from any mcp-capable tool that can connect."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Semantic Search from AI Assistants (Priority: P1)

As a developer using an MCP-capable AI assistant (like Cursor or Windsurf), I want to search my engram memories directly from the chat interface so that I can quickly retrieve relevant context and notes without leaving my IDE.

**Why this priority**: This is the core value proposition of the feature - making engram's data accessible to external AI tools.

**Independent Test**: Can be tested by configuring the MCP server in a tool like Cursor and asking the AI to "search my engram for [topic]". It should return relevant results.

**Acceptance Scenarios**:

1. **Given** the MCP server is running and connected to a client, **When** a search tool is called with a query "how to use semantic search", **Then** the system returns a list of relevant memory snippets from the engram store.
2. **Given** the engram store contains specific notes, **When** a query matches those notes semantically, **Then** those notes appear in the top results.

---

### User Story 2 - Easy Configuration and Connection (Priority: P2)

As a user, I want to easily connect the engram MCP server to any MCP-capable application by providing a simple command-line entry point so that I can start using it with minimal setup.

**Why this priority**: Essential for usability and adoption; if users cannot easily connect their tools, the search functionality is useless.

**Independent Test**: Can be verified by adding the server command to an MCP client's configuration file (e.g., `mcpServers` in Cursor) and confirming the connection status is "active".

**Acceptance Scenarios**:

1. **Given** a standard MCP client, **When** the engram MCP server command is added to the configuration, **Then** the client successfully initializes the server over the appropriate transport.
2. **Given** the server is starting, **When** it cannot find the engram database, **Then** it provides a clear error message to the MCP client.

---

### User Story 3 - Rich Metadata in Results (Priority: P3)

As a researcher, I want the search results to include metadata like timestamps and source URLs so that I can verify the context and origin of the information retrieved.

**Why this priority**: Increases the utility of the search results by providing provenance and temporal context.

**Independent Test**: Can be tested by inspecting the result of a search tool call and verifying the presence of fields like `timestamp`, `source`, and `content`.

**Acceptance Scenarios**:

1. **Given** a successful search result, **When** viewed in the client interface, **Then** the user sees the primary content along with its original source or creation date.

---

### Edge Cases

- **Empty Results**: What happens when a search query returns no matches in the engram store? (The system should return a friendly "no results found" message rather than an error).
- **Database Locked**: How does the system handle concurrent access if another process is writing to the database?
- **Large Result Sets**: How does the system handle queries that could return hundreds of matches? (Should implement a default limit or pagination).
- **Missing Database**: How does the system behave if the engram storage directory does not exist or is empty?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement a Model Context Protocol (MCP) server.
- **FR-002**: System MUST expose a tool named `search_engram` (or similar) to connected MCP clients.
- **FR-003**: The `search_engram` tool MUST accept a `query` parameter (string) and an optional `limit` parameter (integer).
- **FR-004**: System MUST perform semantic search against the existing engram store.
- **FR-005**: Search results MUST be returned as an array of objects, including content and available metadata (e.g., source, tags).
- **FR-006**: System MUST handle initialization and provide server capabilities (tools list) upon connection.
- **FR-007**: System MUST provide clear error logging for troubleshooting connection issues.

### Key Entities *(include if feature involves data)*

- **Engram Memory**: Represents a single unit of stored information, including the text content, embedding (for search), and metadata.
- **MCP Tool**: The interface definition exposed to external clients, defining parameters and return types for the search operation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A connected MCP client can retrieve search results for a known topic in under 1 second (excluding network/client overhead).
- **SC-002**: 100% of standard MCP-compliant clients can successfully discover and call the `search_engram` tool.
- **SC-003**: Results returned are semantically relevant to the input query.
- **SC-004**: The server remains stable and responsive over long-lived connections.
