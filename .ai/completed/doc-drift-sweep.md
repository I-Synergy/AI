# Doc Drift Sweep

**Status:** DONE
Started: 2026-09-25
Completed: 2026-09-25

## Steps

- [x] 1. writer: `TEMPLATE-USAGE.md` + `TEMPLATE-FAQ.md` — suite counts, settings comment, template-owned list
- [x] 2. writer: `.ai/tests/{README,TESTING-GUIDE,QUICK-REFERENCE}.md` + README↔work-type-mapping row comparison
- [x] 3. developer: `upgrade-template.py` TEMPLATE_OWNED · `validate-claude-md.py` stale message · `implement-and-review.chain.md` rule count
- [x] 4. writer: `.pi/CONVERSION-SUMMARY.md` + `.pi/SKILLS-README.md` — investigate, then fix or recommend
- [x] 5. orchestration: run suite, commit the sweep
- [x] 6. complete: move progress to `.ai/completed/doc-drift-sweep.md`

## Notes

Scope approved by the user in-session ("fix the doc drift"), covering the cluster mapped by the README
pass plus three one-line corrections of the same class. No separate plan file: the enumerated list
was the approved scope.

**The facts the sweep corrects against** (verified by the README pass):
- `.ai/tests/run-all-tests.sh` runs **11** suites: structure, skills, references, content, tokens,
  claude-md, settings, copilot, smoke, reasonix, pi. It does **not** run `validate-upgrade-script.py`.
- `.ai/tests/test_suite.py` (pytest) runs **12** — the eleven above plus `validate-upgrade-script.py`.
  So "10-suite", "9-suite", "6-suite" and "11-suite" claims are all wrong somewhere.
- `.ai/skills/` holds **37** skill directories; `.ai/agents/` holds **9** agent files.
- `.claude/settings.local.json` **is** tracked (an earlier README comment claimed otherwise).

**Out of scope, deliberately:** the `AGENTS.md` / `DEEPSEEK.md` ownership-policy question — those two
files are in neither `TEMPLATE_OWNED` nor `PROJECT_OWNED`, so downstream projects never receive updates
to them. That is a policy decision for the user, not a correction.

**Anti-pattern this sweep must not repeat:** re-numbering. Every stale count in this repo came from
duplicating a number that lives elsewhere. Prefer deleting a count or pointing at its source over
correcting it.
