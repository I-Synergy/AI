# Harness Health Score

Status: DONE
Started: 2026-10-30

## Steps
- [x] Add `.ai/tests/score-harness.py` (weighted 0–100 scorer with --json / --badge / --from-json / --fail-under)
- [x] Add `.ai/tests/test_score_harness.py` (fast unit tests, no validator execution)
- [x] Add trigger-line and prose-to-skills validators
- [x] Wire new suites into `run-all-tests.sh` and `test_suite.py`
- [x] Document the scorer and validators in `.ai/tests/README.md` and `README.md`
- [x] Publish the score per release (release notes + assets + live README badges)
- [x] Verify: 14/14 bash suites, 15/15 pytest wrappers, 29/29 scorer tests, hygiene-lint clean, diff clean

## Notes
- Plan: `.ai/plans/harness-health-score.md` (approved 2026-10-30).
- Harness² (google-research/harness2) evaluated and deliberately not adopted: it scores benchmark task
  performance (JobBench/LAB/WorkBuddy), not config integrity, and needs Linux + Vertex AI credentials.
- The scorer is a reporting layer over the existing validators; it does not reimplement any check.
- Two new gates: `validate-triggers.py` (11 skills + 8 agents gained trigger clauses) and
  `validate-prose.py` (AGENTS.md blocks over 100 words must point at `.ai/`).
- `sync-platforms.py` always exits 0, so the scorer now reads its change-count summary and
  promotes pending drift to FAIL.
- Two rogue writes by a subagent were reverted: an unrelated `.ai/scripts/sync-platforms.py`
  rewrite (client selection) that nothing in this task asked for.
- Score on a clean tree: 97.2/100, grade A+. The remaining deductions are the pre-existing
  advisories in `validate-content.py` (20), `validate-tokens.sh` (2), `validate-agents-md.py` (4)
  and `smoke-test.py` (15, unknown `Find`/`Ls` tools). They are real findings, not scorer defects;
  left visible rather than suppressed.
