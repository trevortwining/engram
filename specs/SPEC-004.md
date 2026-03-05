# SPEC-004: Engram Skill Bridge

## Status
Draft

## Goal
Define the OpenClaw skill that turns the Engram store into an actionable knowledge source, ensuring agents can query it, stay in sync, and know when reindexing is required.

## Requirements
1. **Store Locator:** The skill must read the `ENGRAM_STORE` environment variable to learn where the current `engram.lancedb` lives. If the variable is missing or the path is not reachable, the skill should fail fast with a clear, dialogue-friendly explanation so the human can fix the configuration.
2. **Query Composer:** Based on the agent or human prompt, the skill should canonicalize what it "wants to learn" (topic, question, decision point) into a concise text query. This can be as simple as stripping filler wording, extracting nouns/verbs, and/or synthesizing a short question that mirrors the intent (e.g., turning "what did I decide about LanceDB" into that searchable phrase).
3. **Search Execution:** The skill must invoke Engram via the existing CLI (`uv run main.py search "<query>" --limit <n>`) using the configured `ENGRAM_STORE`. It should parse the resulting JSON (text/path/line/score) and pass structured context back to whichever agent called it.
4. **Reindex Control:** Whenever something new lands in the store (a file is added/updated or `ENGRAM_STORE` points somewhere new), the skill should both:
   * Emit a clear instruction: *"Content changed—please run `uv run main.py index <path>` before asking again"* so humans know a refresh is ideal.
   * Offer to run the indexing command itself (e.g., `uv run main.py index <path>`) whenever it detects the change and the workload fits within the current policy (e.g., no other heavy jobs). It should record the start time, report how long the reindex took, and mark the store as freshly synced.
5. **Guardrails:** The skill should expose metadata telling the caller how fresh the last search results are (e.g., timestamp), whether a reindex was queued/run, and any pending reminders if the agent was told not to reindex automatically.

## Testing Requirements
- [ ] Simulate missing `ENGRAM_STORE` and confirm the skill returns a friendly error message.
- [ ] Provide a set of natural-language prompts and verify the query composer produces the expected simplified query strings.
- [ ] Mock the CLI output and ensure the skill returns the original JSON structure plus any freshness metadata.
- [ ] Trigger the "new content" path and assert the skill includes the reindex reminder cue in its response so the human knows to re-run the index command.

## Success Criteria
- The skill sits between OpenClaw and Engram, automatically locating the store, composing queries, and returning JSON-ready context.
- Every response carries enough freshness metadata that the orchestrator can decide whether to re-run `uv run main.py index ...` or rely on cached results.
- Humans are explicitly reminded to rerun indexing whenever the store receives new content, keeping the vector database in sync.
