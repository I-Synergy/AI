# Fix: orchestrator.md hard-codes the agent list (issue #53)

## Problem

`.ai/agents/orchestrator.md` ships `agents: [architect, designer, developer, reviewer, security,
tester, ui-developer, ui-tester, writer]`. That list is the template's inventory, not the project's:

1. `validate-adapters.py` TEST 9 requires the list to equal the repo's `.ai/agents/*.md` exactly, so
   any project that installs extra agents (dotnet-maui, its own) fails a template-owned validator.
2. `upgrade-template.py` diffs `.ai/agents/` (template-owned), so the project's correction is
   reported CHANGED and the template's 9-agent list can be written back, re-breaking the validator.

## Decision

Remove the hard-coded inventory instead of generating it.

- VS Code documents that a coordinator permits **all** available agents when `agents` is omitted
  (or `['*']`), and that the field is Local-harness only. An explicit list buys nothing the
  template needs, and any list is wrong for a project that installs agents.
- With no `agents:` key, the file is identical in the template and in every project, so
  `upgrade-template.py` reports it UNCHANGED and cannot revert anything.
- No generated file and no per-project state: nothing new to keep in sync.

## Steps

1. `.ai/agents/orchestrator.md`: drop `agents:`; name the delegation table in `AGENTS.md` as the
   single source of the agent inventory.
2. `.ai/tests/validate-adapters.py`: TEST 9 asserts the coordinator does **not** pin an inventory
   (no `agents:` key, or `['*']`), still requires `disable-model-invocation: true` and a
   delegation tool.
3. `.ai/tests/validate-upgrade-script.py`: regression test — a project with extra agents keeps its
   `orchestrator.md` byte-identical after a non-interactive upgrade.
4. Docs: `.ai/reference/copilot-integration.md`, `README.md`, `TEMPLATE-FAQ.md` where they describe
   the orchestrator's agent list.
5. Run the validation suite; update `README.md`; mark DONE and move the progress file.

## Not touched

`.ai/ai.json` (gitignored, extension state), `CHANGELOG.md` (CI), `.ai/session-context.md`
(placeholder in this repo).
