# VS Code Settings Merge
Status: DONE
**Status:** DONE (2026-11-17)
Started: 2026-11-17

Plan: `.ai/plans/vscode-settings-merge.md`. Spans the template (`D:\Projects\Github\AI`) and the extension (`D:\Projects\Github\AIWorkspaceManager`).

## Steps
- [x] Template: fragments in `.ai/reference/templates/vscode/` and `merge-rules.json`
- [x] Template: upgrade-template.py merges .vscode and .claude settings (comment-preserving, pinned keys, legacy hooks from merge-rules.json); `.vscode/*` out of TEMPLATE_OWNED
- [x] Template: validators and tests for fragments and merge
- [x] Extension: JsoncMerger (text-surgery, comment-preserving) with unit tests
- [x] Extension: InstallAgentConfig merges .vscode settings/tasks and .claude/settings.json; gitignore entries fixed
- [x] Extension: build and tests pass
- [x] Template: sync-platforms links prompt adapters only while `.ai/prompts` has files; validate-adapters TEST 3 updated
- [x] Extension: PlatformMirrorService aligned (generated `.claude/rules`, conditional prompt links, legacy `.claude/instructions` removed)
- [x] Extension: UI reflects the changes (client descriptions, prompt hint, merge outcomes, mirror report)
- [x] Template: full validation suite passes
- [x] Update README.md for the change (template README + copilot-integration.md; extension README + CHANGELOG)

## Notes
- Extension repo has uncommitted user work (MaintenanceService.cs, WorkspaceOperations.cs, ...). Build on it, never revert it.
- Final: template 15\/15 suites, 93 pytest, upgrade 14\/14; extension 265 dotnet tests, 42 JS tests, tsc clean; 31 Python\/C# parity cases byte-identical.
