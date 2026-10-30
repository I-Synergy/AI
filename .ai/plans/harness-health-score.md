# Harness Health Score

Status: DONE (2026-10-30)
Started: 2026-10-30
Requested by: user — "assign a score like from harness2" — weighted 0–100 over the validation suites, template repo only.

## Goal

Turn the existing pass/fail validation harness into a single weighted 0–100 health score with a
per-category breakdown, machine-readable JSON, and a shields.io badge. No validator behaviour
changes: the scorer is a reporting layer that invokes the existing scripts and weights their
results.

## Existing types / assets reused (no duplicates created)

- `.ai/tests/validate-*.{py,sh}`, `smoke-test.py`, `validate-upgrade-script.py` — unchanged
- `.ai/scripts/sync-platforms.py --dry-run` — drift signal, already returns 0/1
- `.ai/scripts/hygiene-lint.py` — process-hygiene signal, already returns 0/1
- Warning convention already used by every validator: `⚠️` lines; `⚠️  SKIP:` means "not applicable"
  and must not cost points
- `.ai/tests/test_suite.py` patterns (`_run_python`, `_run_bash`) — mirrored, not imported

## Scoring model

`score = Σ weight × credit`, credit = `1.0` PASS, `0.8` WARN (exit 0 with at least one `⚠️` line
that is not a SKIP), `0.0` FAIL. Weights sum to 100.

| # | Check | Runner | Category | Weight |
|---|-------|--------|----------|--------|
| 1 | Directory structure | `validate-structure.sh` | Integrity | 6 |
| 2 | Skill frontmatter | `validate-skills.py` | Integrity | 6 |
| 3 | File references | `validate-references.sh` | Integrity | 6 |
| 4 | Content quality | `validate-content.py` | Integrity | 5 |
| 5 | Token consistency | `validate-tokens.sh` | Integrity | 5 |
| 6 | AGENTS.md references | `validate-agents-md.py` | Integrity | 4 |
| 7 | Integration smoke | `smoke-test.py` | Integrity | 4 |
| 8 | Claude settings | `validate-settings.py` | Platform | 5 |
| 9 | Copilot integration | `validate-copilot.py` | Platform | 5 |
| 10 | Platform sync drift | `sync-platforms.py --dry-run` | Platform | 8 |
| 11 | Traceability | `validate-traceability.py` | Quality | 8 |
| 12 | Process hygiene | `hygiene-lint.py` | Quality | 8 |
| 13 | Standards manifest | `validate-standards.py` | Standards | 14 |
| 14 | Release versioning | `validate-release.py` | Release | 8 |
| 15 | Upgrade script | `validate-upgrade-script.py` | Release | 8 |

Grades: A+ ≥95, A ≥90, B ≥80, C ≥70, D ≥60, F <60. Badge colour follows the same bands.

## Files

1. `.ai/tests/score-harness.py` — scorer. Flags: `--json PATH`, `--badge PATH`,
   `--from-json PATH` (re-render saved results, no validators run), `--timeout SECONDS`.
   Console output: per-category table, total, grade, and every deduction named.
2. `.ai/tests/test_score_harness.py` — fast unit tests (synthetic results, weight sum = 100,
   PASS/WARN/FAIL credits, SKIP neutrality, badge colour bands, every declared runner exists).
3. `.ai/tests/README.md` — new "Harness Health Score" section.
4. `README.md` — one line under the validation section pointing at the scorer.
5. `.ai/progress/harness-health-score.md` — progress file; moved to `.ai/completed/` on finish.

Not changed: `run-all-tests.sh` (keeps 12 suites; the scorer re-invokes them, so adding it there
would double runtime for no new coverage) and `test_suite.py`.

## Verification

- `python .ai/tests/score-harness.py` → 100/A+ on the current clean tree, exit 0
- `python -m pytest .ai/tests/test_score_harness.py -q` → all pass
- `python -m pytest .ai/tests/test_suite.py -q` → still 13 passed
- `bash .ai/tests/run-all-tests.sh` → still 12/12
- Break a fixture (temp copy) to prove a failing check docks its weight, then restore
- `python .ai/scripts/hygiene-lint.py` → 0 issues
- `git diff --check` + review final diff for leftovers

## Approval needed

Implemented and verified. See `.ai/completed/harness-health-score.md`.
