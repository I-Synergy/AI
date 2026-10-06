# Plan: Align validators and verify-config with the AGENTS.md layout

Status: APPROVED (decisions answered 2026-10-06)
Date: 2026-10-06

## Problem

The working tree is mid-migration: `AGENTS.md` is now the master instructions file, and
`CLAUDE.md`, `DEEPSEEK.md`, `REASONIX.md`, `.claude/settings.json`, `.claude/settings.local.json`
and `.pi/settings.json` are deleted. `.claude/commands/` and `.agentty/commands/` are new
(generated from `.ai/commands/`, gitignored).

The verification run found 6 of 16 pytest tests failing, plus `validate-settings.py` and
`validate-reasonix.py`/`validate-pi.py` failing standalone. Every failure traces to a validator
or skill that still hard-codes a file that no longer exists. Content validators
(standards, traceability, skills, copilot, hygiene) all pass.

## Decisions (answered by the user 2026-10-06)

1. Deletions are intentional. The template must be **universal** across Claude Code, agentty,
   codewhale and similar tools: `AGENTS.md` is the neutral master and nothing may be
   Claude-specific except tool-specific config files.
2. **Restore the hooks** (option a): a slimmed `.claude/settings.json` from `git show HEAD:.claude/settings.json`.
3. **Retire** the Reasonix and Pi validators (`validate-reasonix.py`, `validate-pi.py`, their
   `test_suite.py` tests and callers). The junction creation in `sync-skills.py` is untouched.

Original question text kept below for the record.

## Decisions needed before any code (user)

1. **Are the deletions intentional?** (`CLAUDE.md`, `DEEPSEEK.md`, `REASONIX.md`, both
   `.claude/settings*.json`, `.pi/settings.json`). This plan assumes yes.
2. **Where did the hooks go?** The deleted `.claude/settings.json` held:
   - `SessionStart` -> `python .ai/scripts/sync-skills.py` (bootstraps junctions on a fresh clone;
     git cannot track junctions)
   - `PostToolUse` re-sync on edits under `.ai/skills/**` and `.ai/agents/**`
   - `PostToolUse` conditional `dotnet build`
   - `plansDirectory: ./.ai/plans`

   Nothing in the tree replaces them (`SessionStart` now appears only in the stale verify-config
   skill and README). `AGENTS.md` still says "The `Stop` hook runs `dotnet build`", which now has
   no config behind it. Options: (a) restore a slimmed `.claude/settings.json` with the hooks,
   (b) document the manual `python .ai/scripts/sync-skills.py` step as the only bootstrap and
   correct the `AGENTS.md` sentence, (c) other tool-specific replacement.
   **Recommendation: (a)** - without it a fresh clone has no junctions.
3. **Which assistants remain supported?** Reasonix and Pi junctions still resolve and their
   validators pass the link checks. Decide whether to keep their validators (minus the
   `REASONIX.md` / `settings.json` checks) or retire them.

Council check (`AGENTS.md`): editing validators, tests and a skill applies no architecture,
public-contract, migration or security-posture change, so no council. Decision 2 (restoring or
dropping hooks) touches nothing in the security model; if the user disagrees, ask a framing
question first.

## Existing files reused (no new types)

Edit in place: `.ai/tests/test_suite.py`, `.ai/tests/validate-settings.py`,
`.ai/tests/validate-reasonix.py`, `.ai/tests/validate-pi.py`, `.ai/tests/validate-structure.sh`,
`.ai/tests/validate-references.sh`, `.ai/tests/validate-tokens.sh`,
`.ai/tests/validate-claude-md.py`, `.ai/tests/validate-deepseek-parity.py`,
`.ai/skills/verify-config/SKILL.md`, `.ai/commands/verify-config.md`, `README.md`,
`TEMPLATE-USAGE.md`, `TEMPLATE-FAQ.md`, `.ai/tests/README.md`. No new scripts.

## Steps

- [x] 1. Resolve decisions 1-3 with the user; record answers in the progress file Notes
- [ ] 2. Inventory every reference to `CLAUDE.md`, `DEEPSEEK.md`, `REASONIX.md`, `.claude/settings*.json`, `.pi/settings.json` across `.ai/tests/`, `.ai/skills/`, `.ai/commands/`, `.ai/scripts/`, `README.md`, `TEMPLATE-*.md`; list in Notes with file:line
- [ ] 3. Rename the `CLAUDE.md` target to `AGENTS.md` in `validate-structure.sh`, `validate-references.sh`, `validate-tokens.sh` and `test_suite.py` (suite 6 and the main-file list); keep the existing assertions on `AGENTS.md` content where they still apply
- [ ] 4. `validate-claude-md.py`: retarget to `AGENTS.md` (or rename to `validate-agents-md.py` and update `run-all-tests.sh` and `test_suite.py` callers)
- [ ] 5. `validate-settings.py`: allow `commands` in `.claude/`; make a missing `settings.json` a SKIP only if decision 2 is (b), otherwise require the hooks from decision 2(a)
- [ ] 6. `validate-reasonix.py` and `validate-pi.py`: drop the `REASONIX.md` and `.pi/settings.json` existence checks (per decision 3); keep the junction, `runAs: subagent` and stale-subdirectory checks
- [ ] 7. `validate-deepseek-parity.py`: confirm it still SKIPs cleanly with no `DEEPSEEK.md`, and that its message names the reason
- [ ] 8. Rewrite `verify-config/SKILL.md` and `.ai/commands/verify-config.md`: master file is `AGENTS.md`; remove the `DEEPSEEK.md`/`REASONIX.md` sections (3c, 3e); keep junction-link, `.gitignore` (add `.claude/commands/`, `.agentty/commands/`), agent-roster and tier-alias checks; add the `.claude/commands` and `.agentty/commands` generation check; update the Output Format table
- [ ] 9. Fix `AGENTS.md` / `README.md` / `TEMPLATE-*.md` statements the inventory shows to be wrong (notably the `Stop` hook sentence and the "run once after cloning" instructions), per decision 2
- [ ] 10. Mirror any edit to `AGENTS.md` per the DeepSeek-profile memory only if `CLAUDE.md.deepseek-backup` still exists; otherwise note it is moot
- [ ] 11. Verify (see below)

## Delegation

- Steps 2-7: `developer` subagent (Python/shell edits, runs the validators).
- Step 8: `writer` subagent (skill and command prose).
- Step 9: `writer` subagent.
- Review: `reviewer` subagent over the full diff, checking that no validator was weakened to pass
  (a check may be removed only if its target is gone by decision, never loosened).
- Every subagent prompt carries the progress-file Edit instructions from `AGENTS.md`.

## Verification

Run from the repo root with `PYTHONIOENCODING=utf-8`:

- `python -m pytest -q -p no:cacheprovider` -> 16 passed
- `python .ai/tests/validate-settings.py`, `validate-reasonix.py`, `validate-pi.py`,
  `validate-standards.py`, `validate-traceability.py`, `validate-skills.py`,
  `validate-copilot.py` -> exit 0
- `python .ai/scripts/hygiene-lint.py` -> 0 issues
- `validate-content.py` warnings: triage separately; not in scope unless caused by this change
- Fresh-clone check (if hooks restored): clone to `.ai/tmp/`, run the bootstrap command, confirm
  the junction targets resolve.

No `dotnet build` is involved. If any subagent builds anyway, it must set
`MSBUILDDISABLENODEREUSE=1` and pass `-nodeReuse:false`.

## Risks

- Removing a check can hide a real regression. Mitigation: reviewer step and the rule above.
- `.claude/` is partly gitignored; do not commit generated `commands/` content.
- Per memory: do not write session state to `.ai/session-context.md` in this template repo.
- Working tree has 45 uncommitted changes from the in-flight migration. Do not mix this work into
  that change set silently; confirm with the user whether to commit the migration first.

## Done when

All verification commands pass, the progress file is marked DONE and moved to
`.ai/completed/agents-md-validator-alignment.md`.
