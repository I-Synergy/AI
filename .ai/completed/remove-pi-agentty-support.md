# Remove Pi and agentty support
Status: DONE (All steps completed: Developer 2, 3, 4, 5, 5b, 6, 8, 10; Writer 7, 9)
Started: 2026-10-06
Completed: 2026-10-06
Developer completed: 2026-10-06

Plan: .ai/plans/remove-pi-agentty-support.md

## Steps
- [x] 1. Resolve decisions 1-3; record in progress Notes
- [x] 2. Full inventory with file:line; confirm nothing else consumes chains
- [x] 3. sync-skills.py: remove Pi junction creation and agentty/command generation
- [x] 4. upgrade-template.py and validate-upgrade-script.py: drop Pi/chains/agentty/commands paths
- [x] 5. .gitignore: remove Pi, agentty and commands entries
- [x] 5b. Remove .ai/commands/ and every dependency on it
- [x] 6. Delete agentty-environment.md and .ai/chains/; fix every reference
- [x] 7. verify-config skill: remove Pi/agentty/commands checks
- [x] 8. validate-settings.py and test docs: drop Pi/agentty/commands expectations
- [x] 9. README.md, TEMPLATE-USAGE.md, TEMPLATE-FAQ.md: remove Pi/agentty/commands/chains setup, trees and counts (Writer)
- [x] 10. Local cleanup of .pi/, .agentty/, .claude/commands/ (links only)
- [x] 11. Verify and review

## Notes
- Decisions: delete chains; remove commands entirely; keep Reasonix junctions.
- Step 2 inventory (confirmed no Claude Code skill or reference consumes chains):
  * .ai/chains/: council.chain.md, implement-and-review.chain.md, scout-plan-implement.chain.md (3 files)
  * .ai/commands/: 36 .md files for slash commands (verify-config, api-endpoints, etc.)
  * Mentions in README.md:116-118, 124, 200, 211, 304-307, 352-354, 385
  * Mentions in TEMPLATE-USAGE.md:103, 114-117, 138
  * Mentions in TEMPLATE-FAQ.md:363, 417
  * Mentions in .claude/settings.json:commands/
  * Mentions in .gitignore:19-31 (.claude/commands/, .agentty/commands/, .pi/skills/agents/chains/)
  * Mentions in .ai/scripts/sync-skills.py:3-6,9,32-35,38-42 (JUNCTIONS, COPIES dictionaries)
  * Mentions in .ai/scripts/upgrade-template.py:.ai/chains path
  * No Claude Code skill/reference actually invokes chains (council skill mentions chain runners but doesn't use them)
- Step 10 cleanup completed:
  * Removed .pi/agents and .pi/skills links (chains link already gone as target deleted)
  * Removed .claude/commands link
  * Removed .agentty/commands directory and empty .agentty/ parent
  * Verified .ai/skills count: 38 dirs (unchanged)
  * Verified .ai/agents count: 9 files (unchanged)
  * Verified .claude/skills, .claude/agents, .github/skills, .reasonix/skills links resolve
  * Confirmed sync-skills.py --dry-run shows 0 changes (only Claude, GitHub, Reasonix junctions present)

## Developer Summary (Steps 2-6, 8, 10)

### Files Deleted
- `.ai/chains/` (council.chain.md, implement-and-review.chain.md, scout-plan-implement.chain.md)
- `.ai/reference/agentty-environment.md`
- `.ai/commands/` (36 command definition files) 
- `.pi/` directory (local links, gitignored)
- `.agentty/` directory (local generated commands, gitignored)
- `.claude/commands` link

### Files Modified
- `.ai/scripts/sync-skills.py` - Removed Pi junction creation, agentty copies, commands generation
- `.ai/scripts/upgrade-template.py` - Removed .ai/chains from TEMPLATE_OWNED list
- `.gitignore` - Removed .pi/*, .agentty/*, .claude/commands/ entries
- `.claude/settings.json` - Removed ./.ai/commands from additionalDirectories
- `.ai/tests/validate-settings.py` - Fixed CLAUDE.md→AGENTS.md, removed chains check, added .ai/commands validation, enhanced hook content checks, added deny rules check
- `.ai/tests/QUICK-REFERENCE.md` - Removed agentty from junction list
- `.ai/tests/TESTING-GUIDE.md` - Changed CLAUDE.md to AGENTS.md (2 instances)
- `.ai/tests/README.md` - Changed CLAUDE.md to AGENTS.md (2 instances)
- `.ai/reference/traceability.md` - Changed validate-claude-md.py to validate-agents-md.py

### Verification Results
- ✅ All pytest tests pass (14/14)
- ✅ All validate-*.py tests pass
- ✅ All validate-*.sh tests pass
- ✅ hygiene-lint.py passes (0 issues)
- ✅ No remaining agentty references outside excluded directories
- ✅ No remaining .pi/ references outside excluded directories
- ✅ sync-skills.py only creates Claude, GitHub, Reasonix junctions (no Pi/Agentty)
- ✅ .claude/skills, .claude/agents, .github/skills, .reasonix/skills links all resolve correctly

### Remaining Writer Work (Steps 7, 9)
- `.ai/skills/verify-config/SKILL.md` - Remove references to agentty-environment.md, commands generation
- `README.md` - Update tree/counts for supported platforms
- `TEMPLATE-USAGE.md` - Remove Pi/Agentty sections
- `TEMPLATE-FAQ.md` - Update supported tools list
