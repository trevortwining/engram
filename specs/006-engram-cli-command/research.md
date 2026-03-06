# Research: `engram` CLI Command

## DECISION-001: Distribution via `[project.scripts]` in `pyproject.toml`

### Decision
Implement the `engram` command by defining a console script entry point in `pyproject.toml` that points to the `app` instance in the main script.

### Rationale
- **Simplicity**: Directly supported by `uv` and standard Python packaging tools.
- **Local Portability**: Fulfills the requirement of running the command without `uv run` by allowing it to be installed as a global tool using `uv tool install`.
- **Minimal Changes**: Requires only configuration changes in `pyproject.toml` and a slight restructure of the main entry point to be a callable function.

### Alternatives Considered
- **Shell Aliases**: Rejected because they are shell-specific and harder to manage across different environments or for AI agents.
- **shiv/PyInstaller**: Rejected as overkill for a local-only tool where the user already has a working `uv` environment.
- **Custom Wrapper Scripts**: Rejected in favor of the standardized Python approach which handles pathing and dependency resolution more reliably.

---

## DECISION-002: Project Layout Transition

### Decision
Transition from a flat file layout (`main.py` at root) to a standard `src/` layout (`src/engram/main.py`).

### Rationale
- **Packaging Best Practices**: The `src/` layout prevents accidental imports of development tools and is the recommended structure for packages intended to be installed as tools.
- **Entry Point Clarity**: Makes the entry point path (`engram.main:main`) unambiguous for the `[project.scripts]` configuration.

---

## DECISION-003: Entry Point Implementation

### Decision
Modify `main.py` to ensure the `typer` app is callable as a standard Python function (e.g., `main()`).

### Rationale
- Console scripts require a callable function without arguments.
- Ensures the `if __name__ == "__main__":` block is mirrored in the tool's execution.
