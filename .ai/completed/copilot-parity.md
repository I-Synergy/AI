# Copilot Parity
Status: DONE
**Status:** DONE (2026-11-17)
Started: 2026-11-17

Plan and council record: `.ai/plans/copilot-parity.md`. Superseded Phase B steps are overridden by the council's Decision section.

## Steps
- [x] Workspace settings: `chat.useAgentsMdFile: false` in `.vscode/settings.json`; `.vscode/tasks.json` run on demand (no folderOpen)
- [x] Copilot runtime section: `.ai/reference/copilot-runtime.md`, emitted by `sync-instructions.py` into `copilot-instructions.md`
- [x] Agents: each body lists the skill and rule files to read first
- [x] Scoped instructions added to `.ai/instructions/` (C#, tests, .ai workspace)
- [x] Prompts converted to skills; `.ai/prompts` removed; ai.json updated
- [x] sync-platforms.py: copy-only `.claude/rules` generator, retire prompt and `.claude/instructions` links, log `_rmdir` failures
- [x] Shared hook scripts in `.ai/scripts/hooks/` wired in `.claude/settings.json` (portable launcher, path self-filter, Claude-only build, probe log)
- [x] upgrade-template.py: ship new paths, regenerate copilot-instructions, replace legacy hook commands
- [x] Validators added and wired into run-all-tests.sh and CI
- [x] Full validation suite passes
- [x] Update README.md for the change (plus copilot-integration.md, TEMPLATE-FAQ.md, TEMPLATE-USAGE.md, sync-platforms SKILL.md)
- [x] Workspace settings round 2: customAgents.enabled, useClaudeHooks, pinned instruction/skill loading
- [x] Coordinator agent `.ai/agents/orchestrator.md` for Copilot (agent tool + agents list), ai.json, validator
- [x] Terminal build env in `.vscode/settings.json` (`terminal.integrated.env.*` mirrors `.claude/settings.json` env)
- [x] Copilot runtime text and docs: orchestrator usage, correct `chat.useAgentsMdFile` scope (Local harness only), new settings
- [x] Build-before-final-reply line in `copilot-runtime.md` (mimics the Claude Stop hook)
- [x] Full validation suite passes (round 2)

## Notes
- Do not write project state to `.ai/session-context.md` (template ships it as a placeholder).
