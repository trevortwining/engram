# Contract: MCP Tool Schema

The Engram MCP server exposes the following tools to connected clients.

## Tool: `search_engram`

**Description:** Search the user's engram memory store using semantic similarity to find relevant notes, context, and snippets.

### Input Schema (JSON Schema)
```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The natural language query or concept to search for in the engram memory store."
    },
    "limit": {
      "type": "integer",
      "description": "Maximum number of results to return. Defaults to 10 if not provided.",
      "default": 10
    }
  },
  "required": ["query"]
}
```

### Output Format
The tool returns an array of MCP `TextContent` objects. Each object contains the search result formatted as a readable string, including metadata.

Example Output Content:
```text
Source: notes/architecture.md
Timestamp: 2026-03-01T12:00:00Z
Similarity: 0.92

The architecture uses a local-first approach with LanceDB for vector storage...
```
