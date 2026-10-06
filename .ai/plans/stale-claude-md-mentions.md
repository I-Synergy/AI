# Plan: Fix stale CLAUDE.md mentions

Status: APPROVED (user: "fix stale claude.md mentions", 2026-10-06)
Date: 2026-10-06

## Classification (from the inventory)

Stale - describes THIS template's layout, must become AGENTS.md:
- `.ai/reference/copilot-integration.md` (tree, config-file table, work-type mapping, precedence statement)
- `.ai/reference/operational-rules.md` lines 24-26
- `.ai/reference/task-execution.md` line 111
- `.ai/skills/solution-generator/SKILL.md` lines 57, 93
- `.ai/skills/upgrade-template/SKILL.md` description, "What Gets Synced" table (CLAUDE.md and REASONIX.md rows)
- `.ai/scripts/upgrade-template.py` docstring line 6, argparse description line 286, and the
  TEMPLATE_OWNED list: lists CLAUDE.md and REASONIX.md (both gone) and NOT AGENTS.md, so the
  upgrade would never ship the master file to downstream projects

Legitimate - downstream projects built from an older template may still own a CLAUDE.md:
- `.ai/scripts/migrate-to-ai.py` (migrates an old `.claude/` layout; keep CLAUDE.md handling, also handle AGENTS.md)
- `.ai/tests/validate-upgrade-script.py` fixture (a legacy project CLAUDE.md must never be touched)

## Decision applied (not new): the template layout change already made CLAUDE.md -> AGENTS.md.
The upgrade tool follows it: AGENTS.md becomes template-owned (copied if new, diffed if changed,
never silently overwritten); a legacy CLAUDE.md/REASONIX.md/DEEPSEEK.md in a target is left
untouched and documented as a manual merge. Additive for downstream consumers; no council.

## Steps
- [ ] 1. upgrade-template.py: TEMPLATE_OWNED swaps CLAUDE.md -> AGENTS.md, drops REASONIX.md; fix docstring and description; legacy files never read or written
- [ ] 2. migrate-to-ai.py: rewrite paths in AGENTS.md as well as CLAUDE.md when present; messages accurate
- [ ] 3. validate-upgrade-script.py: keep the legacy CLAUDE.md untouched assertion; add: AGENTS.md is shipped to a target that has none, and a changed target AGENTS.md is diffed, not overwritten in --non-interactive
- [ ] 4. Docs: copilot-integration.md, operational-rules.md, task-execution.md, solution-generator skill, upgrade-template skill (add a short "migrating from CLAUDE.md" note)
- [ ] 5. Verify (pytest, validators, hygiene-lint, final grep) and review

## Verification
pytest and every validator pass; `grep -rn "CLAUDE\.md\|CLAUDE\.MD"` outside plans/completed/progress
shows only migrate-to-ai.py, the upgrade-script test fixture/comments and the one migration note.
