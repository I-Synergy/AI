# Plan: Remove Pi and agentty support

Status: APPROVED (2026-10-06)
Date: 2026-10-06

## Problem

The user asked to drop Pi and agentty. The template currently supports them through:

- `.ai/scripts/sync-skills.py`: creates `.pi/{skills,agents,chains}` junctions and generates
  `.agentty/commands/` (real files; agentty does not follow junctions) from `.ai/commands/`
- `.gitignore`: entries for the `.pi/` junction targets and `.agentty/commands/`
- `.ai/reference/agentty-environment.md`: agentty-only reference doc
- `.ai/chains/*.chain.md` (3 files): reachable only through the `.pi/chains` junction
- `.ai/skills/verify-config/SKILL.md` (6 mentions), `README.md` (14), `TEMPLATE-USAGE.md` (3),
  `TEMPLATE-FAQ.md` (1), `.ai/tests/QUICK-REFERENCE.md` (1), `validate-settings.py`,
  `upgrade-template.py` (chains)
- On disk: `.pi/` and `.agentty/` directories (gitignored junction/generated content)

This reverses the earlier "universal template" wording; the docs should say which tools remain
supported (Claude Code and GitHub Copilot, plus any tool that reads `AGENTS.md`).

## Decisions (answered 2026-10-06)

1. Delete `.ai/chains/` (after confirming no Claude Code skill or reference runs a chain).
2. **Remove commands entirely**: delete `.ai/commands/`, stop generating `.claude/commands/` and
   `.agentty/commands/`, drop the `commands` allowance in `validate-settings.py` and the
   `./.ai/commands` entry in `.claude/settings.json`, and remove every doc mention.
3. Keep Reasonix junction creation untouched.

Original question text kept below.

## Decisions needed (user)

1. **`.ai/chains/`** - only Pi consumes them. Delete the folder (recommended) or keep as plain docs?
   Check first that no skill or reference tells Claude Code to run a chain; the council plans
   mention chains.
2. **`.ai/commands/` and `.claude/commands/`** - `.ai/commands/` exists mainly to feed agentty
   (`.agentty/commands/`) and now also `.claude/commands/`. Keep the Claude Code slash-command
   generation (recommended) or drop commands entirely?
3. **Reasonix** - already stripped of validators. Leave its junction creation alone (assumed),
   or remove it too?

Council check: removing two integrations is not an architecture, contract, migration or
security-posture change. No council.

## Existing files reused

No new types. Edit in place: `.ai/scripts/sync-skills.py`, `.ai/scripts/upgrade-template.py`,
`.gitignore`, `README.md`, `TEMPLATE-USAGE.md`, `TEMPLATE-FAQ.md`,
`.ai/skills/verify-config/SKILL.md`, `.ai/commands/verify-config.md`,
`.ai/tests/QUICK-REFERENCE.md`, `.ai/tests/validate-settings.py`. Delete:
`.ai/reference/agentty-environment.md`, `.ai/chains/` (per decision 1).

## Steps

- [x] 1. Resolve decisions 1-3; record in progress Notes
- [ ] 2. Full inventory with file:line (exclude vendored hugo theme assets, where "pi" is unrelated text); confirm nothing else consumes chains
- [ ] 3. sync-skills.py: remove Pi junction creation and agentty command generation; keep Claude and Copilot links; make the script remove nothing it did not create
- [ ] 4. upgrade-template.py and validate-upgrade-script.py: drop Pi/chains/agentty paths from copy and diff lists
- [ ] 5b. Remove .ai/commands/, the command generation in sync-skills.py, the commands allowance in validate-settings.py and the ./.ai/commands entry in .claude/settings.json
- [ ] 5. .gitignore: remove `.pi/*` and `.agentty/commands/` entries; keep `.claude/commands/` if decision 2 keeps it
- [ ] 6. Delete `.ai/reference/agentty-environment.md` and, per decision 1, `.ai/chains/`; fix every reference to them
- [ ] 7. verify-config skill and command: remove Pi/agentty checks; update the supported-tools list
- [ ] 8. validate-settings.py and test docs: drop Pi/agentty expectations
- [ ] 9. README.md, TEMPLATE-USAGE.md, TEMPLATE-FAQ.md: remove Pi/agentty setup, trees and counts; state the supported tools
- [ ] 10. Local cleanup of `.pi/` and `.agentty/` (gitignored, so not in the repo): list contents first; they hold junctions, so remove the links only, never the targets
- [ ] 11. Verify and review

## Delegation

- Steps 2-5, 8: `developer`. Step 6-7, 9: `writer` (after step 2's inventory). Review: `reviewer`.
- Every prompt carries the progress-file Edit instructions from `AGENTS.md`.

## Verification

- `python -m pytest -q -p no:cacheprovider`, every `.ai/tests/validate-*.py`,
  `python .ai/scripts/hygiene-lint.py` all pass.
- `grep -rIi "agentty\|\.pi/\|claude-pi" .` outside `.git`, `.ai/plans`, `.ai/completed` and the
  vendored hugo theme returns nothing.
- Run `python .ai/scripts/sync-skills.py` in a scratch clone: creates only the supported links.

## Risks

- Step 10 deletes junctions. Windows `Remove-Item -Recurse` on a junction can follow it and
  delete `.ai/skills`. Use `cmd /c rmdir` on each link, and verify `.ai/skills` count afterwards.
  Note the `Bash(rm -rf:*)` deny rule blocks `rm -rf`.
- A chain that Claude Code skills reference would break; step 2 checks this before deletion.
- Working tree still holds uncommitted migration and alignment changes; keep this work separable.

## Done when

All verification passes, progress file marked DONE and moved to
`.ai/completed/remove-pi-agentty-support.md`.
