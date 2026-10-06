# Fix stale CLAUDE.md mentions
**Status:** DONE
Started: 2026-10-06
Completed: 2026-10-06

Plan: .ai/plans/stale-claude-md-mentions.md

## Steps
- [x] 1. upgrade-template.py ownership list and wording
- [x] 2. migrate-to-ai.py handles AGENTS.md as well as CLAUDE.md
- [x] 3. validate-upgrade-script.py assertions
- [x] 4. Docs: copilot-integration, operational-rules, task-execution, solution-generator, upgrade-template skill
- [x] 5. Verify and review (all steps complete)

## Notes
- Developer owns 1-3 (scripts + test); writer owns 4 (docs/skills). Disjoint files.

## Step 4 Verification (Writer)

### Files Changed
1. `.ai/reference/copilot-integration.md`:
   - Line 9: Architecture tree → AGENTS.md (instead of CLAUDE.md)
   - Line 40: Config comparison table → both systems load AGENTS.md
   - Line 109: "Update CLAUDE.md" → "Update AGENTS.md if needed"
   - Line 169: "Claude (via CLAUDE.md)" → "Claude (via AGENTS.md)"
   - Line 223: Precedence statement → reflect single master AGENTS.md

2. `.ai/reference/operational-rules.md`:
   - Lines 24-26: CLAUDE.md references → AGENTS.md

3. `.ai/reference/task-execution.md`:
   - Line 111: "this CLAUDE.md" → "this AGENTS.md"

4. `.ai/skills/solution-generator/SKILL.md`:
   - Line 57: Reference architecture location updated
   - Line 93: "CLAUDE.md Critical Coding Rules" → "AGENTS.md Critical Coding Rules"

5. `.ai/skills/upgrade-template/SKILL.md`:
   - Frontmatter: Neutral description (removed "CLAUDE.MD template")
   - Lines 78-84: "What Gets Synced" table → removed REASONIX.md and CLAUDE.md rows, added AGENTS.md
   - New section: "Migrating from CLAUDE.md" with instructions for legacy files

### Verification Results
- ✅ pytest: 13 tests pass
- ✅ validate-skills.py: 37 skills validated, 0 errors
- ✅ validate-structure.sh: 47 checks pass, 0 fail
- ✅ validate-references.sh: 19 checks pass, 0 fail
- ✅ grep check: Only migration note mentions CLAUDE.md (expected)

## Verification Results

### Step 1: upgrade-template.py
Changes made:
- Line 6-9 (docstring): Updated to reflect AGENTS.md as template-owned, legacy files left untouched
- Line 38 (TEMPLATE_OWNED): Removed "REASONIX.md", kept ".reasonix"
- Line 59 (TEMPLATE_OWNED): Replaced "CLAUDE.md" with "AGENTS.md"
- Line 286 (argparse): Changed "CLAUDE.MD template" to "AI template"

### Step 2: migrate-to-ai.py
Changes made:
- Lines 217-230: Loop over both "CLAUDE.md" and "AGENTS.md", processing each if present
- Accurate per-file messages including "not found - skipping" case
- Behavior for CLAUDE.md unchanged (backward compatible)

### Step 3: validate-upgrade-script.py
Changes made:
- Line 203-204: Added comment clarifying legacy project file
- Lines 320-364: Added test_agents_md_shipped_to_empty_target() - verifies AGENTS.md copied when target has none
- Lines 367-405: Added test_agents_md_not_overwritten_in_non_interactive() - verifies changed AGENTS.md is skipped
- Test list updated to include both new tests

### Test Results
All 13 tests pass:
- TEST 1-9: Original tests pass
- TEST 10: AGENTS.md shipped to empty target ✓
- TEST 11: AGENTS.md not overwritten in non-interactive ✓
- TEST 12-13: Remaining original tests pass ✓

### Validator Results
- validate-upgrade-script.py: 13/13 PASS
- validate-agents-md.py: PASS
- validate-skills.py: All 37 skills validated, 0 errors
- validate-structure.sh: 47 checks passed, 0 failed (AGENTS.md recognized)
- validate-content.py: PASS with warnings
- validate-references.sh: 19 checks passed, 0 failed (AGENTS.md references verified)
- hygiene-lint.py: 0 issues

### Files Changed
1. .ai/scripts/upgrade-template.py (4 changes across docstring, TEMPLATE_OWNED list, argparse)
2. .ai/scripts/migrate-to-ai.py (1 change: Step 3 loop over config files)
3. .ai/tests/validate-upgrade-script.py (3 changes: legacy comment, 2 new tests, test list update)

All changes complete and verified.
