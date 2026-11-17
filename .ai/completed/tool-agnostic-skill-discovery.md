# Tool-Agnostic Skill Discovery
Status: DONE
Started: 2026-11-16

## Steps
- [x] Confirm the hard constraint from the VS Code bundle (no `.ai` skill location exists)
- [x] Make sync-platforms.py tool-driven with `--tools` and CONFLICT guard
- [x] Add `.agents/skills` adapter for other skills-standard agents
- [x] Auto-create adapters on VS Code folder open (.vscode/tasks.json)
- [x] Extend validate-copilot.py with `.agents/skills` and single-source checks
- [x] Update README, TEMPLATE-USAGE, TEMPLATE-FAQ (Q10), copilot-integration, sync-platforms and verify-config skills
- [x] Run the validation suite
- [x] Update README.md for the change and move this file to .ai/completed/

## Notes
Decision: keep one copy in `.ai/` and expose it through per-tool links. No agent reads
`.ai/` directly, and no setting can add it, so an adapter path per tool family is
mandatory. Content duplication stays at zero; the only visible duplication is VS Code's
Customizations editor listing each adapter path it scans.
