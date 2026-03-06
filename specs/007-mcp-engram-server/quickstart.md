# Quickstart: MCP Engram Server

This guide explains how to connect your MCP-capable client (like Cursor, Windsurf, or Claude Desktop) to the Engram local memory store.

## Prerequisites
- Python 3.12+
- The `engram` CLI installed and initialized (an existing `engram.lancedb` directory).

## Installation
Ensure you have installed engram with the necessary dependencies. In your local environment:
```bash
pip install -e .
```
*(Assuming the MCP server dependencies like the `mcp` package are added to pyproject.toml)*

## Configuration in AI Assistants

### Cursor
Add the following to your Cursor MCP settings (`Cursor Settings -> Features -> MCP -> + Add New MCP Server`):
- **Name**: `engram-memory`
- **Type**: `command`
- **Command**: `engram`
- **Args**: `mcp`

*(Alternatively, you can edit Cursor's `mcp.json` config directly).*

### Claude Desktop
Edit your `claude_desktop_config.json` file:
```json
{
  "mcpServers": {
    "engram": {
      "command": "engram",
      "args": ["mcp"]
    }
  }
}
```

## Testing the Connection
Once configured, open your AI assistant and ask:
> "Use the search_engram tool to find out what our architecture principles are."

The assistant should invoke the tool, query your local LanceDB store, and return context-aware answers based on your notes.
