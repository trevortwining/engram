# Feature Specification: `engram` CLI Command

**Feature Branch**: `006-engram-cli-command`  
**Created**: 2026-03-05  
**Status**: Draft  
**Input**: User description: "Update the spec so that it only references the change to running the engram command. The dependencies on lanceDB and uv are fine. this is a local tool that will only be run on my machine."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Direct Command Execution (Priority: P1)

As a local user of Engram, I want to type `engram [arguments]` in my terminal instead of `uv run main.py [arguments]` so that I can interact with my memory engine more efficiently.

**Why this priority**: Primary goal of the feature is to simplify the CLI invocation.

**Independent Test**: Can be tested by executing `engram --help` from any directory (after installation) and seeing the correct command output.

**Acceptance Scenarios**:

1. **Given** the tool is installed, **When** I run `engram version`, **Then** it returns the current version without needing `uv run`.
2. **Given** the tool is installed, **When** I run `engram query "search terms"`, **Then** it performs the retrieval and displays results.

---

### User Story 2 - Local Environment Installation (Priority: P2)

As a user on a single local machine, I want to install the `engram` command once using `uv` so that it is globally available in my user shell.

**Why this priority**: Enables the direct command usage.

**Independent Test**: Verify that `engram` is found in the shell PATH after a `uv tool install` or equivalent local installation.

**Acceptance Scenarios**:

1. **Given** the project source, **When** I install it as a tool via `uv`, **Then** the `engram` command becomes available in the PATH.

---

### Edge Cases

- **Missing `uv`**: Since the user stated `uv` dependencies are fine, we assume the user has `uv` available for the initial installation/setup.
- **Path Conflicts**: If another `engram` command exists on the system, the user might need to manage their PATH or use an alias.
- **Development vs. Global**: Ensure that developers can still run the script directly if needed during development.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a console script entry point named `engram`.
- **FR-002**: The `engram` command MUST expose all functionality currently available in `main.py`.
- **FR-003**: System MAY depend on `uv` for installation and runtime environment management (e.g., via `uv tool install` or similar).
- **FR-004**: System MUST maintain compatibility with LanceDB as the primary storage engine.
- **FR-005**: System MUST be optimized for local-only execution on the user's machine.

### Key Entities

- **Console Entry Point**: The configuration in `pyproject.toml` that maps the `engram` command to the Python logic.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can successfully execute `engram` command from a terminal window without specifying the path to `main.py`.
- **SC-002**: 100% functional parity with the existing `main.py` script.
- **SC-003**: Installation takes less than 2 minutes using standard `uv` commands.
- **SC-004**: No external cloud dependencies introduced; remains 100% local.
