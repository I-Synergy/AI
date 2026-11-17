# Remove Reasonix Support
Status: DONE
Started: 2026-11-16

## Steps
- [x] Drop `.reasonix` junction targets and cleanup support in sync-platforms.py
- [x] Remove `.reasonix` from upgrade-template.py TEMPLATE_OWNED
- [x] Remove `.reasonix` entries from .gitignore
- [x] Update README.md, TEMPLATE-USAGE.md, TEMPLATE-FAQ.md (new Q9)
- [x] Update AGENTS.md and regenerate .github/copilot-instructions.md
- [x] Update session-management, task-execution, handoff template, session-context placeholder
- [x] Update sync-platforms, verify-config, upgrade-template, product-discovery skills
- [x] Run the validation suite
- [x] Update README.md for the change and move this file to .ai/completed/

## Notes
Reasonix Code is no longer supported, so `.reasonix/skills` and `.reasonix/agents`
are removed. `sync-platforms.py` now deletes those junctions when it finds them, which
migrates existing projects without a manual step. `.ai/plans/product-discovery-skill.md`
is a historical plan and keeps its original wording.
