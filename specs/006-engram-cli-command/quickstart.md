# Quickstart: `engram` CLI Command

## Local Installation

1.  Ensure you have `uv` installed.
2.  From the project root, run:
    ```bash
    uv tool install --editable .
    ```
    This will install the `engram` command into your shell's PATH and link it to the current directory for ongoing development.

3.  Verify installation:
    ```bash
    engram --help
    ```

## Usage

### 1. Indexing a Directory
```bash
engram index ./docs
```

### 2. Searching Memory
```bash
engram search "how to use engram" --limit 3
```

## Maintenance
To update the tool as you develop, simply run the installation command again or rely on the `--editable` link.
