# Skill Body Slimming — 10 Oversized SKILL.md Files

**Status:** DONE — see `.ai/completed/skill-body-slimming.md` for the result, gates and deviations
**Slug:** skill-body-slimming

---

## Why

`agentty skills` lints every installed skill and warns when a **SKILL.md body** (lines *after* the
YAML frontmatter) exceeds 500 lines:

```
warn: body is 676 lines (spec recommends ≤ 500 — move detail to references/)
```

Ten skills trip it. `hugo` proves the counter is frontmatter-exclusive — 526 total lines but a
57-line frontmatter (469 body → clean) — while `winui-specialist` is 520 total with a 7-line
frontmatter (513 body → flagged). Nine of the ten surface in the agentty catalog; `devops-engineer`
carries `disable-model-invocation`, is hidden from the catalog, and is therefore the tenth warning
the user never sees reported.

| Skill | Body lines | of which code | `references/` today |
|---|---|---|---|
| security | 1498 | 1129 | none |
| software-security | 1160 | 826 | none |
| maui-specialist | 903 | 656 | none |
| devops-engineer *(hidden)* | 839 | 618 | none |
| blazor-specialist | 818 | 580 | none |
| integration-specialist | 812 | 607 | none |
| performance-engineer | 750 | 469 | none |
| api-security | 677 | 405 | none |
| database-migration | 529 | 262 | none |
| winui-specialist | 513 | 148 | none |

8,499 always-loaded lines, ~5,700 of them verbatim C#/YAML. **Not one of the ten has a
`references/` directory** — which is the entire point of the rule: SKILL.md is the routing document,
`references/` carries the detail. The two healthy skills do the opposite of the ten: `api-endpoints`
is 86 body lines with 4 references, `hugo` is 469 body lines with 6.

A contributing smell: seven of the ten already tell the agent to load repo patterns
(`## Load Additional Patterns` → `.ai/patterns/api-patterns.md`, 44 KB) and then inline 400–600
lines of the same class of sample code anyway.

This is not a defect in the repo's own validators — `validate-skills.py` (37/37) and
`hygiene-lint.py` (0 issues) both pass. The complaint is purely agentty's size lint.

## Scope

Restructure ten SKILL.md files: keep the routing surface (Role, Expertise, Critical Rules, Common
Pitfalls, Checklist), move every code-heavy H2 into `references/*.md`, and leave pointer lines.
Target body ≤ **300** lines per skill — comfortably under the 500 lint and matching the shape of
`api-endpoints`.

## Blast radius

Ten files rewritten, ~48 reference files created. No content deleted, none summarised.

| # | Skill | Body → | Reference files created |
|---|---|---|---|
| 1 | `security` | 1498 | `zero-trust.md`, `compliance.md`, `incident-response-and-dr.md`, `risk-and-vulnerability.md`, `cloud-security.md`, `devsecops-and-monitoring.md`, `encryption-and-pki.md`, `training-and-awareness.md` |
| 2 | `software-security` | 1160 | `injection-and-csrf.md`, `authentication.md`, `secrets-and-dependencies.md`, `code-review-and-sast.md`, `threat-modeling.md`, `logging-and-file-upload.md` |
| 3 | `maui-specialist` | 903 | `project-and-blazor-hybrid.md`, `local-database.md`, `data-synchronization.md`, `platform-specific.md`, `mvvm-and-lifecycle.md` |
| 4 | `devops-engineer` | 839 | `dockerfile.md`, `azure-pipelines.md`, `github-actions-and-iac.md`, `secrets-and-health.md` |
| 5 | `blazor-specialist` | 818 | `components.md`, `forms-and-services.md`, `state-and-interop.md`, `authentication-and-performance.md` |
| 6 | `integration-specialist` | 812 | `http-client-and-webhooks.md`, `message-queues.md`, `oauth2.md`, `rate-limits.md` |
| 7 | `performance-engineer` | 750 | `profiling.md`, `database-queries.md`, `caching.md`, `async-memory-and-latency.md`, `load-testing-and-monitoring.md` |
| 8 | `api-security` | 677 | `owasp-top-10.md`, `input-validation.md`, `secrets-and-audit-logging.md`, `authorization.md` |
| 9 | `database-migration` | 529 | `commands-and-entity-config.md`, `seeding-and-data-migration.md`, `indexing-and-performance.md`, `multi-tenant.md`, `postgres-full-text.md` |
| 10 | `winui-specialist` | 513 | `build-and-run.md`, `xaml-correctness.md`, `mvvm-review.md`, `msix-packaging.md`, `ui-automation-testing.md`, `wpf-migration.md` |

Each row is one independent unit of work (one skill, one directory) — delegated one agent per skill.

`.ai/skills/security/SKILL.md` also carries a **pre-existing structural bug** the split should
retire: `## Incident Response Planning`, `## Penetration Testing Coordination`, `## Disaster Recovery
and Business Continuity`, and `## Security Awareness and Training` each contain "sections" that use
`##` instead of `###` (`## 1. Preparation` → `## 7. Post-Incident`, `## Scope`, `## Timeline`,
`## Mandatory Training (All Employees)`, …), flattening 31 H2s that are really 4 topics. Demote them
to `###` inside their reference file.

## Reused, not duplicated (rule 12)

- The `api-endpoints` layout as the reference implementation — its `## References` section, its
  per-workflow `see references/x.md` pointers, and its 86-line body are the shape being copied.
- The `hugo` skill as the second data point for the frontmatter-vs-body distinction.
- `.ai/patterns/*.md` — the ten skills' `## Load Additional Patterns` pointers stay exactly as they
  are and keep pointing at the shared pattern files. Nothing is copied out of `.ai/patterns/`.
- The repo's own validators are **not** modified — this change is about satisfying agentty's lint,
  not about loosening it.

## Gates

1. `agentty skills` → 0 warnings, "37 skill(s), 0 warning(s)".
2. Body ≤ 300 lines for each of the ten.
3. **Content preservation** — every H2/H3 heading and every fenced code block that existed in the
   original SKILL.md exists somewhere under `.ai/skills/<name>/` afterwards. Checked against
   `git show HEAD:<path>` per skill; a missing heading or a shortened fence fails the gate.
4. Frontmatter byte-identical for all ten except `winui-specialist` (verify: it has a 7-line
   frontmatter; no change intended).
5. Relative links (`.ai/patterns/...`, `.ai/reference/...`) still resolve — `validate-references.sh`.
6. `bash .ai/tests/run-all-tests.sh` → all suites pass (run from inside the workspace; the suite
   `cd`s to its own directory and the sandbox blocks that, so run the sub-validators directly and
   note the deviation).
7. `python3 .ai/tests/validate-skills.py` → 37/37, 0 errors. `hygiene-lint.py` → 0 issues.

No commit unless asked.

## Notes

- The ten files stay the single canonical copy: `.claude/`, `.github/`, `.reasonix/`, and `.pi/`
  skills are symlinks/junctions to `.ai/skills/` (`.ai/scripts/sync-skills.py`), so each split is
  visible to every platform with no sync step.
- `devops-engineer` is included even though the catalog hides it — it is a real warning, and leaving
  it out would make the fix look complete when it is not.
