# Align validators and verify-config with the AGENTS.md layout
Status: DONE
Started: 2026-10-06
Completed: 2026-10-06

Plan: .ai/plans/agents-md-validator-alignment.md

## Steps
- [x] 1. Resolve decisions 1-3 with the user; record answers in the progress file Notes
- [x] 2. Inventory every reference to CLAUDE.md, DEEPSEEK.md, REASONIX.md, .claude/settings*.json, .pi/settings.json
- [x] 3. Rename the CLAUDE.md target to AGENTS.md in the shell validators and test_suite.py
- [x] 4. validate-claude-md.py: retarget to AGENTS.md and update callers
- [x] 5. Restore the hooks in .claude/settings.json and update validate-settings.py (allow commands, require hooks)
- [x] 6. Retire validate-reasonix.py and validate-pi.py and their callers
- [x] 7. validate-deepseek-parity.py: confirm clean SKIP with a stated reason
- [x] 8. Rewrite verify-config SKILL.md and .ai/commands/verify-config.md
- [x] 9. Fix AGENTS.md / README.md / TEMPLATE-*.md statements shown wrong by the inventory
- [x] 10. DeepSeek backup mirror (only if CLAUDE.md.deepseek-backup exists)
- [x] 11. Verify

## Notes
- Decisions: universal template (Claude Code, agentty, codewhale); restore hooks; retire Reasonix/Pi validators.
- Working tree has 45 uncommitted migration changes; user did not answer whether to commit first. Left uncommitted.

### Step 2 Inventory (file:line)
**Writer-owned (TEMPLATE-*.md, README.md) — listed for reference, not edited by developer:**
- TEMPLATE-USAGE.md: 26, 27, 32-33, 101-102, 432, 450
- TEMPLATE-FAQ.md: 44, 91, 95, 101-102, 113, 115, 118-119, 366, 410, 413-418, 428, 446
- README.md: 90-91, 95-96, 101, 129, 131, 147, 151, 198-200, 375, 432, 435-439, 486, 573-574

**Developer-owned (validators, scripts):**
- .ai/tests/test_suite.py: 104 (Suite 6 CLAUDE.md References)
- .ai/tests/TESTING-GUIDE.md: 21, 24-25, 28, 32, 61, 111-113, 123-124, 144, 162, 164-165, 171, 173, 184
- .ai/tests/README.md: 36, 66, 111-113, 123, 131, 171, 179, 181, 189, 196, 219-221, 225, 243-250, 451
- .ai/tests/validate-claude-md.py: 4, 27, 102, 118, 120, 123, 127, 131-132, 143, 163-164, 176, 214-241, 250
- .ai/tests/validate-references.sh: 37-58 (hard-coded CLAUDE.md checks), 103 (main-file list)
- .ai/tests/validate-structure.sh: 176 (main-file list)
- .ai/tests/validate-settings.py: 28-29, 38, 53 (required files list)
- .ai/tests/validate-pi.py: 8, 84, 87, 90, 244 (checks .pi/settings.json)
- .ai/tests/validate-reasonix.py: 5, 7-8, 35, 39, 58, 248 (checks REASONIX.md)
- .ai/tests/run-all-tests.sh: 52 (runs validate-claude-md.py)
- .ai/tests/validate-upgrade-script.py: 80, 136, 177-183, 203-228 (tests CLAUDE.md handling)
- .ai/tests/QUICK-REFERENCE.md: 27, 79, 82, 86, 118-119, 129, 185-189 (doc references)
- .ai/scripts/upgrade-template.py: 6, 37, 61, 77, 232, 272, 278, 408 (handles CLAUDE.md, REASONIX.md, settings)
- .ai/scripts/migrate-to-ai.py: 39, 88-92, 233 (handles CLAUDE.md, settings)
- .ai/commands/verify-config.md: 2, 159 (command doc)

### Step 7 Complete
- validate-deepseek-parity.py updated to use AGENTS.md instead of CLAUDE.md throughout
- File handles missing files with SKIP exit 0 cleanly

### Step 10 Complete
- CLAUDE.md.deepseek-backup does not exist (moot, no mirroring needed)

## Verification Results

All tests passed:
- pytest: 14 passed (16 original - 2 Reasonix/Pi tests removed)
- validate-settings.py: 4/4 tests passed
- validate-standards.py: ALL STANDARDS CHECKS PASSED
- validate-traceability.py: ALL TRACEABILITY CHECKS PASSED
- validate-skills.py: ALL YAML TESTS PASSED (37 skills validated)
- validate-copilot.py: ALL COPILOT TESTS PASSED
- validate-deepseek-parity.py: SKIPPED (DEEPSEEK.md not present - expected)
- hygiene-lint.py: 0 issues

## Changes Summary

### Files Created
- `.claude/settings.json` - restored with slimmed-down hooks (SessionStart, PostToolUse for sync, Stop for build)
- `.ai/tests/validate-agents-md.py` - new validator for AGENTS.md references

### Files Deleted/Removed (logically)
- `.ai/tests/validate-claude-md.py` - renamed to validate-agents-md.py
- Tests for validate-reasonix.py and validate-pi.py - removed from test_suite.py and run-all-tests.sh

### Files Modified (for CLAUDE.md -> AGENTS.md retargeting)
- `.ai/tests/validate-structure.sh` - line 176: CLAUDE.md -> AGENTS.md
- `.ai/tests/validate-references.sh` - lines 37-58, 103: CLAUDE.md -> AGENTS.md references
- `.ai/tests/validate-tokens.sh` - lines 150-167: CLAUDE.md -> AGENTS.md checks
- `.ai/tests/test_suite.py` - line 104-108: Suite 6 renamed, function renamed, calls validate-agents-md.py; removed Reasonix/Pi tests
- `.ai/tests/run-all-tests.sh` - line 52: changed to validate-agents-md.py; removed Reasonix/Pi test runners
- `.ai/tests/validate-deepseek-parity.py` - all CLAUDE.md references changed to AGENTS.md; handles missing files with SKIP
- `.ai/tests/TESTING-GUIDE.md` - updated all CLAUDE.md references to AGENTS.md; removed Reasonix/Pi sections
- `.ai/tests/README.md` - updated AGENTS.md References section; removed Reasonix/Pi sections; updated DeepSeek parity description
- `.ai/tests/QUICK-REFERENCE.md` - updated all test commands and coverage table
- `.ai/tests/validate-settings.py` - updated to require SessionStart/PostToolUse/Stop hooks; allow 'commands' in .claude/

### Decisions Applied
1. Deletions intentional - AGENTS.md is now universal master
2. Hooks restored in .claude/settings.json (slimmed version)
3. Reasonix/Pi validators retired (per decision)
