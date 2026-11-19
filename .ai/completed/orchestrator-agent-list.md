# Orchestrator agent list (issue #53)
Status: DONE
**Status:** DONE (2026-11-19)
Started: 2026-11-19

Plan: `.ai/plans/orchestrator-agent-list.md`

## Steps
- [x] Remove the hard-coded `agents:` list from `.ai/agents/orchestrator.md`
- [x] Rewrite validate-adapters.py TEST 9 to reject a pinned inventory
- [x] Add an upgrade regression test for a project with extra agents
- [x] Update docs that describe the orchestrator's agent list
- [x] Run the validation suite
- [x] Update README.md for the change

## Notes
- Root cause: template-owned file carries project-specific inventory.
- Fix: omit `agents:` (VS Code then permits all available agents).
- Verification: validate-adapters 10/10, validate-upgrade-script 15/15, pytest 93 passed,
  run-all-tests 14/15 — `validate-release.py` fails inside `run-all-tests.sh` only, identically on
  the unmodified tree (passes standalone), so it is pre-existing and unrelated.
- The new TEST 9 was checked against the old hard-coded list: it fails, as intended.
- `.github/copilot-instructions.md` regenerated (runtime block wording changed).
