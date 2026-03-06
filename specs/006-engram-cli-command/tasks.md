# Tasks: `engram` CLI Command

**Input**: Design documents from `/specs/006-engram-cli-command/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create source directory structure `src/engram/`
- [X] T002 [P] Create `src/engram/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [X] T003 Move `main.py` to `src/engram/main.py`
- [X] T004 Update `src/engram/main.py` to include a `main()` entry point that calls `app()`
- [X] T005 Update `pyproject.toml` to include `[project.scripts]` entry for `engram = "engram.main:main"`

---

## Phase 3: User Story 1 - Direct Command Execution (Priority: P1) 🎯 MVP

**Goal**: Enable running the `engram` command directly from the terminal

**Independent Test**: Run `engram --help` from a different directory and see the correct output.

### Implementation for User Story 1

- [X] T006 [US1] Install the tool locally in editable mode using `uv tool install --editable .`
- [X] T007 [US1] Verify `engram version` returns functional parity with existing script
- [X] T008 [US1] Verify `engram index` functionality with a test directory
- [X] T009 [US1] Verify `engram search` functionality and JSON output contract

**Checkpoint**: At this point, the `engram` command should be fully functional and testable independently

---

## Phase 4: User Story 2 - Local Environment Installation (Priority: P2)

**Goal**: Ensure the tool can be easily installed and managed locally

**Independent Test**: Verify the installation instructions in `quickstart.md` work as expected.

### Implementation for User Story 2

- [X] T010 [US2] Update `README.md` to point to the new `engram` command usage
- [X] T011 [US2] Verify `uv tool list` shows `engram` as an installed tool

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T012 [P] Remove the original `main.py` from the root directory (if still present)
- [X] T013 Update `.gitignore` if necessary to reflect the new `src/` layout
- [X] T014 Run `quickstart.md` validation one last time

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Depends on User Story 1 completion for verification

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test `engram` command independently

### Incremental Delivery

1. Complete Setup + Foundational → Command structure ready
2. Add User Story 1 → Test independently → MVP!
3. Add User Story 2 → Test documentation and management
