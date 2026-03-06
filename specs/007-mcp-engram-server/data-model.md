# Data Model: MCP Engram Server

## Entities

### `SearchQuery` (Tool Argument)
- `query` (string, required): The natural language query to search for.
- `limit` (integer, optional, default=10): Maximum number of results to return.

### `SearchResult` (Tool Return Type)
The MCP search tool will return a list of text objects. Each text object will represent a matched memory snippet.
Fields represented in the formatted text content:
- `content` (string): The raw text of the memory snippet.
- `source` (string): The original file or URL source of the memory.
- `timestamp` (string/datetime): When the memory was ingested or created.
- `score` (float): The semantic similarity score from LanceDB.

## State Transitions
- **Uninitialized**: Server process started, dependencies not yet loaded.
- **Ready**: `lancedb` connection established, embedding model loaded into memory, stdio transport listening for MCP requests.
- **Searching**: Active tool call in progress.
- **Terminated**: Client disconnected via stdio, process exits.
