# Contract: `engram` CLI Command

## Command: `engram`

The `engram` command is the main entry point for the tool.

### Subcommands

#### 1. `index`
Index a directory of Markdown files into the LanceDB database.

**Arguments**:
- `path` (String, required): The directory path to index.

#### 2. `search`
Search the memory database for a specific query.

**Arguments**:
- `query` (String, required): The search query.

**Options**:
- `--limit` (Integer, default: 5): The maximum number of results to return.

## Output Contract (Search Results)
The `search` subcommand MUST return a JSON-formatted list of objects to stdout.

**Schema**:
```json
[
  {
    "text": "The content of the chunk",
    "path": "path/to/source/file.md",
    "score": 0.123
  }
]
```
