# Plan: Remove DeepSeek support (PowerShell backend profile and parity validator)

Status: APPROVED (user chose "remove it" on 2026-10-06 for the options: retarget / retire / leave)
Date: 2026-10-06

## Problem

`CLAUDE.md` and `DEEPSEEK.md` no longer exist, so the DeepSeek swap in
`powershell/Microsoft.PowerShell_profile.ps1` would recreate or overwrite a deleted file. The whole
profile is the DeepSeek backend (its only other function, `claude`, clears the DeepSeek variables),
so retiring the swap retires the profile. Anything validating or documenting it goes too.

## Scope (existing files; no new types)

Delete: `powershell/` (profile + README), `.ai/tests/validate-deepseek-parity.py`.
Edit: `.ai/tests/test_suite.py` (Suite 15), `.ai/tests/run-all-tests.sh` (test 12),
`.ai/tests/{README,TESTING-GUIDE,QUICK-REFERENCE}.md`, `.github/workflows/validate-template.yml`
(parity step), `.gitignore` (`CLAUDE.md.deepseek-backup`), `README.md` (tree line, validator row),
`AGENTS.md` (line 5 "claude, copilot or deepseek"; the sentence pointing at the profile's backend
mapping), `.ai/skills/verify-config/SKILL.md` if it mentions the profile or concrete model names.
Outside the repo: the user-level memory note about the DeepSeek profile swap (now false).
Not touched: `$HOME\.deepseek\credentials.ps1` and the user's own `$PROFILE` (machine state; tell the user).

Council: removal of an optional integration; not an architecture, contract, migration or
security-posture change. No council.

## Steps

- [ ] 1. Inventory every DeepSeek/powershell-profile reference (file:line), including the agent `model:` tier-alias rule that cites the profile
- [ ] 2. Delete powershell/ and validate-deepseek-parity.py; remove Suite 15 and the run-all-tests/CI steps; fix the suite numbering text where it names counts
- [ ] 3. Update test docs, .gitignore and the verify-config skill
- [ ] 4. Update README.md and AGENTS.md (reword the tier-alias note so it no longer points at the deleted profile; do not touch Critical Coding Rules)
- [ ] 5. Verify and review

## Verification

pytest, every `.ai/tests/validate-*.py`, `.ai/scripts/hygiene-lint.py` pass;
`grep -rIi "deepseek" .` outside `.git`, `.ai/plans`, `.ai/completed`, `.ai/progress` is empty;
CI workflow YAML still parses and has no step referencing a deleted script.

## Risks

- The suite count changes again (pytest 14 -> 13). Docs quoting counts must follow.
- AGENTS.md says the profile defines the concrete model per tier slot; that statement must be
  reworded, not just deleted, or the tier-alias rule loses its explanation.
