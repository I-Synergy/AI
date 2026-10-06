# Stop Hook and Orphan Validators Fix

Status: DONE
Started: 2026-10-06
Completed: 2026-10-06

## Summary

Fixed the Stop hook in .claude/settings.json to use proper bash syntax instead of invalid Watch/exists notation, and cleaned up orphan validator files.

## Steps

- [x] Fix Stop hook in .claude/settings.json (replace if/Watch/exists with proper bash command)
- [x] Adjust validate-settings.py assertions if needed for Stop hook (no changes needed - only checks that Stop key exists)
- [x] Test Stop hook command logic in scratch dir (logic verified: exits early if no .sln, checks marker, uses MSBUILDDISABLENODEREUSE)
- [x] Delete orphan files: validate-reasonix.py, validate-pi.py, validate-claude-md.py
- [x] Confirm validate-agents-md.py is proper replacement (functionally identical, targets AGENTS.md instead of CLAUDE.md)
- [x] Grep repo for remaining mentions of orphan validators and fix them
- [x] List any remaining CLAUDE.md references not in upgrade-template.py etc
- [x] Run final tests: pytest, validate scripts, hygiene-lint

## Changes Made

1. **Fixed .claude/settings.json Stop hook:**
   - Replaced invalid `if` field with proper bash `set -e; ... fi` command
   - Logic: checks for *.sln or *.slnx existence, compares marker with src/tests file times
   - On success, touches .ai/tmp/lastbuild-success marker
   - Uses MSBUILDDISABLENODEREUSE=1 and -nodeReuse:false as required
   - No error suppression (no || true)

2. **Deleted orphan validator files:**
   - .ai/tests/validate-reasonix.py (Reasonix integration checks)
   - .ai/tests/validate-pi.py (.pi/ junction checks)
   - .ai/tests/validate-claude-md.py (replaced by validate-agents-md.py)

3. **Updated README.md references:**
   - Line 329: validate-claude-md.py → validate-agents-md.py
   - Lines 333-334: Removed validate-reasonix.py and validate-pi.py entries from file tree
   - Lines 417, 421-422: Removed three validator table rows

4. **Verified validate-agents-md.py is proper replacement:**
   - Functionally identical assertions to validate-claude-md.py
   - Only difference: targets AGENTS.md instead of CLAUDE.md
   - Already integrated in run-all-tests.sh (line 52)

## Final Test Results

All tests passed successfully:
- `python -m pytest -q -p no:cacheprovider` -> 14 passed in 43.36s
- `python .ai/tests/validate-settings.py` -> 4/4 tests passed
- `python .ai/tests/validate-agents-md.py` -> Core tests passed (warnings about orphaned skills/patterns expected)
- `python .ai/tests/validate-standards.py` -> 5/5 tests passed
- `python .ai/tests/validate-traceability.py` -> 0 artifacts (expected for template)
- `python .ai/tests/validate-skills.py` -> 37 skills validated, 0 errors
- `python .ai/tests/validate-deepseek-parity.py` -> Correctly skips (DEEPSEEK.md not present)
- `python .ai/scripts/hygiene-lint.py` -> Clean (duplicate slug warning disappears when progress file moved to completed)

## Remaining References (Not Modified - Per Task Instructions)

All remaining references are in planning/completed/reference files (out of scope):
- .ai/plans/security-agent.md:26-27 (references validate-reasonix.py and validate-pi.py)
- .ai/plans/council-principle.md:53,56,105,154 (references validate-claude-md.py and validate-reasonix.py)
- .ai/plans/compliance-wave-1.md:142,225,227,274,316,404 (references validate-claude-md.py)
- .ai/plans/agents-md-validator-alignment.md:14,24,58,60,69,71,92 (planning doc)
- .ai/completed/agents-md-validator-alignment.md:12,14,35,39,40,41 (completed work doc)
- .ai/completed/doc-drift-sweep.md:11 (completed work doc)
- .ai/completed/compliance-wave-1.md:112,159 (completed work doc)
- .ai/reference/traceability.md:289 (reference doc - not touched per instructions)
