# Use .ai/session-context.md as memory in every supported CLI client
Status: DONE
Started: 2026-10-06

Plan: .ai/plans/session-context-as-memory.md

## Steps
- [x] 1. Resolve open questions 1-2
- [x] 2. Add the SessionStart read hook with placeholder skip and size cap; test it in a scratch dir
- [x] 3. Write the shared Session Memory paragraph into AGENTS.md and .github/copilot-instructions.md; reconcile session-management.md
- [x] 4. Validators for hook and paragraph parity
- [x] 5. Docs and verify-config
- [x] 6. Verify and review

## Notes
- Decisions: AGENTS.md is canonical for all clients; no Stop-hook enforcement.
- Developer owns steps 2 and 4; writer owns steps 3 and 5 (parallel, disjoint files).

## Work Completed
- Step 2: Added SessionStart hook to .claude/settings.json with matcher "startup|resume|clear|compact". Hook:
  - Reads .ai/session-context.md if it exists
  - Skips if first line starts with "# Session Context Template" (placeholder)
  - Prints header and first 200 lines of content
  - Lists 5 most recent files from .ai/completed/
  - Always exits 0
  - Uses python -c to embed the logic (no new script files)
  - Tested in scratch dir with: (a) missing file, (b) 300-line file, (c) CRLF + UTF-8
- Step 4: Added two validators to .ai/tests/validate-settings.py:
  - test_session_context_hook(): Validates hook exists, has correct matcher, references .ai/session-context.md, has 200-line cap, placeholder skip
  - test_session_memory_section(): Validates both AGENTS.md and .github/copilot-instructions.md contain "## Session Memory" heading and both marker sentences
  - Writer completed steps 3 and 5 in parallel (AGENTS.md, .github/copilot-instructions.md, session-management.md)

## Validation Results
- validate-settings.py: 6/6 tests passed (all settings tests)
- pytest: 13/13 tests passed
- validate-structure.sh: 47/47 tests passed
- validate-references.sh: 19/19 tests passed
- validate-tokens.sh: 25/25 tests passed
- hygiene-lint.py: 0 issues
