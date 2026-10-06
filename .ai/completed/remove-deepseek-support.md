# Remove DeepSeek support
Status: DONE
Started: 2026-10-06
Completed: 2026-10-06

Plan: .ai/plans/remove-deepseek-support.md

## Steps
- [x] 1. Inventory every DeepSeek/powershell-profile reference
- [x] 2. Delete powershell/ and validate-deepseek-parity.py; remove Suite 15 and the run-all-tests/CI steps
- [x] 3. Update test docs, .gitignore and the verify-config skill
- [x] 4. Update README.md and AGENTS.md
- [x] 5. Verify and review

## Notes
**Inventory (file:line):**
- AGENTS.md:5 - "You are powered by AI (claude, copilot or deepseek)"
- AGENTS.md:78 - "the concrete model behind each slot is defined by the backend profile in `powershell/Microsoft.PowerShell_profile.ps1`"
- AGENTS.md:157 - backticked runtime path ".ai/tmp/lastbuild-success" (defect to fix)
- .ai/tests/test_suite.py:162-166 - Suite 15 — DeepSeek Parity
- .ai/tests/run-all-tests.sh:58 - Test 12 line with "12. DeepSeek Parity"
- .gitignore:16 - CLAUDE.md.deepseek-backup
- .github/workflows/validate-template.yml:58-59 - Run DeepSeek parity validation step
- README.md:206-208 - powershell/ tree entry with "Anthropic ↔ DeepSeek backend switcher" comment
- README.md:403 - validate-deepseek-parity.py validator row in table
- .ai/tests/README.md:212-226 - "### DeepSeek Parity" section with usage
- .ai/tests/TESTING-GUIDE.md:30 - Table row for DeepSeek Parity
- .ai/tests/QUICK-REFERENCE.md:45-46 - "# DeepSeek parity" section with command
- .ai/skills/verify-config/SKILL.md:45 - Mentions "powershell/Microsoft.PowerShell_profile.ps1"
- powershell/ - entire directory to delete
- .ai/tests/validate-deepseek-parity.py - file to delete
