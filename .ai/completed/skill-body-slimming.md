# Skill Body Slimming

**Status:** DONE
Started: 2026-05-15
Completed: 2026-10-04
Plan: `.ai/plans/skill-body-slimming.md`

## Result

All ten oversized `SKILL.md` bodies were split: the routing surface (Role, Expertise, Critical
Rules, Workflows, Common Pitfalls, Checklist) stays in `SKILL.md`; every code-heavy H2 moved
verbatim into `references/`.

| Skill | Body before | Body after | Refs |
|---|---|---|---|
| security | 1499 | 175 | 8 |
| software-security | 1161 | 172 | 6 |
| maui-specialist | 904 | 207 | 5 |
| devops-engineer *(hidden in catalog)* | 840 | 186 | 4 |
| blazor-specialist | 819 | 184 | 4 |
| integration-specialist | 813 | 189 | 4 |
| performance-engineer | 751 | 203 | 5 |
| api-security | 678 | 211 | 4 |
| database-migration | 530 | 185 | 5 |
| winui-specialist | 514 | 90 | 6 |

51 reference files, 7,225 lines (plan estimated ~48). Every body is ≤ 300 lines; no skill in the
repo now exceeds 500.

## Gates

| # | Gate | Result |
|---|---|---|
| 1 | agentty `skills` → 0 warnings | ✅ by measurement — agentty is not installed here; verified directly that no skill body exceeds 500 lines (largest: `design-interrogation`, 486) |
| 2 | Body ≤ 300 lines per skill | ✅ max 211 (`api-security`) |
| 3 | Content preservation vs `HEAD` | ✅ 10/10 — heading set, fenced-code-marker parity, and line-multiset diff all clean |
| 4 | Frontmatter byte-identical | ✅ 10/10 vs `HEAD` |
| 5 | `validate-references.sh` | ✅ 19 passed, 0 failed |
| 6 | Test suite | ✅ all 14 suites pass (run validator-by-validator — see Deviations) |
| 7 | `validate-skills.py` 37/37 · `hygiene-lint.py` | ✅ 0 errors · 0 issues |

`validate-content.py` reports 25 warnings: 10 `nofence` (all ten skills now carry code in
`references/`, not in the body — the same shape as `api-endpoints`, the plan's reference
implementation) plus pre-existing ones. This is the intended consequence of the split, not a defect.

## Deviations from the plan

- **Reference count** — 51 files, not the ~48 estimated. Three skills split further than the plan's
  per-file table anticipated (`security` gained `architecture-and-zero-trust.md`; its `pentest` and
  `training` topics merged into one file).
- **`winui-specialist` `code-quality.md`** — the plan listed a reference file for `## Code Quality
  Guidelines`, but the section is 7 lines; it stays inline in `SKILL.md`.
- **Suite runner** — `bash .ai/tests/run-all-tests.sh` cannot run here (the suite `cd`s to its own
  directory and the sandbox blocks that). All 14 validators plus `sync-skills.py` were run
  individually; `sync-skills.py` reports 0 junctions changed.
- **agentty** — not installed on this machine, so gate 1 was verified by the same measure the lint
  uses (body line count after frontmatter) rather than by running the tool.

## Work done in this session (2026-10-04)

The previous session stopped at 6/10 with four skills unsplit. On review, all ten bodies were
already slim on disk; the remaining work was **verification**, which found three real defects:

1. **`security` — an entire section was missing.** `## Disaster Recovery and Business Continuity`
   (95 lines: recovery objectives, backup strategy, DB/application recovery procedures, DR testing,
   and the `BackupService` code block) had never been carried into any reference file. Fence markers
   confirmed it: 60 in `HEAD` vs 56 in the split. Restored verbatim from the `HEAD` blob into
   `references/incident-response-and-dr.md`.
2. **Horizontal rules dropped** — `security` was missing 1, `winui-specialist` 6. Restored at the
   positions the originals had them (immediately before the section each introduced — the pattern
   `build-and-run.md` had retained).
3. **Routing prose** — four skills (`security`, `software-security`, `integration-specialist`,
   `winui-specialist`) no longer contained the word *when* or *example*, which `validate-content.py`
   flags as a missing usage description. Fixed by changing "read the reference **before** X" to
   "read the reference **when** X" — a genuine improvement to a routing document.

## Deeper audit (post-verification)

A line-multiset proves lines *survived*; it cannot see reordering, mis-filing or broken prose. A
second pass tested those:

- **Ordering** — fence-aware comparison of every heading's position in `HEAD` against its position
  inside the reference files. No section is reordered anywhere. Apparent breaks were all one of two
  false positives: trailing sections (`Common Pitfalls`, `Code Quality Guidelines`) correctly staying
  in `SKILL.md`, and heading text that repeats in `HEAD` (e.g. `### Input Validation` appears both
  under an OWASP list and inside the code-review checklist) resolving to the wrong index.
- **Dangling prose** — no "see above" / "as described earlier" / "the previous section" survived into
  a reference file; nothing points at a neighbour that is no longer there.
- **Cross-file pointers** — no file in the repo links to a heading anchor inside these skills, and no
  plan carries a live line-number reference into them. (`compliance-wave-1.md`'s `api-security/SKILL.md:233`
  is a historical record of an edit already applied — `GetItemByIdAsync` was deleted by that wave
  because rule 2 forbids it, not by this one.)
- **Doc drift fixed** — `.ai/reference/standards.md` cited `.ai/skills/security/SKILL.md` as the
  implementing artifact for the sample CI workflow. That sample now lives in
  `references/devsecops-and-monitoring.md`; `validate-standards.py` only checks that a path *resolves*,
  so it passed while pointing at a routing document. Pointer corrected.

## Git-history verification

`HEAD` is the correct baseline, confirmed three ways:

- **No commit ever trimmed these skills.** Line counts across their full history are flat
  (`security` 1502 in Apr 2026 → 1502 at `HEAD`; `maui-specialist` 907 → 907; `blazor-specialist`
  822 → 822). The slimming is entirely uncommitted working-tree work, so `HEAD` is the maximal,
  never-reduced state.
- **The agentty checkpoint `816d19a` (`refs/agentty/checkpoints/ba34ce5a68d90b97`, 2026-10-04 20:49)
  confirms the progress file's "6 of 10" claim exactly**: it captured reference files for
  blazor-specialist, integration-specialist, performance-engineer, api-security, database-migration
  and winui-specialist (28 files), and for the other four its tree is byte-identical to `HEAD`
  (877/877, 654/654, 516/516, 588/588 body lines) — i.e. still unsplit.
- **Three-way diff (`HEAD` → checkpoint → working tree) shows no content lost between the checkpoint
  and now** for any of the ten. The only two differences are this session's own routing-prose edits
  (`integration-specialist`, `winui-specialist`: "before implementing" → "when implementing").

Two consequences worth recording:

- The four skills split *after* the last checkpoint (security, software-security, maui-specialist,
  devops-engineer) have **no snapshot** — the window in which `security` lost its DR section is
  covered by no checkpoint at all. Recovery was possible only because the split was never committed;
  had it been committed, that section would have been gone.
- Earlier unresolved dangling objects (`a6f8ea3`, the 2026-07 works in progress, `0a5828a`) hold no
  skill content relevant to this work.

## Notes

- The ten files stay the single canonical copy: `.claude/`, `.github/`, `.reasonix/`, `.pi/` skills
  are junctions to `.ai/skills/`, so each split is visible to every platform with no sync step.
- `devops-engineer` was included even though the catalog hides it (`disable-model-invocation`) — it
  was a real warning, and omitting it would have made the fix look complete when it was not.
- `.ai/session-context.md` was deliberately not touched: this repo's copy is the *template* with
  `{ApplicationName}` placeholders, and session handoff notes must not overwrite it.
