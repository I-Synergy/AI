# Dependency Refresh and Repository Review

Status: DONE
Started: 2026-10-27
Owner: Reasonix Code

## Goal

Bring every external dependency this repository actually declares up to a current
release, and review the repository for drift, stale references and hygiene issues.

## What the repository actually depends on

There is no Node.js project, `package.json`, lockfile or .NET solution here — the
template is Markdown, Python validation scripts and CI workflows. Its external
dependencies are therefore:

| Dependency | Where declared | Current | Target |
|---|---|---|---|
| `actions/checkout` | `.github/workflows/*.yml`, skill examples | v4 (v1/v2 in examples) | v7 |
| `actions/setup-python` | `.github/workflows/validate-template.yml`, docs | v5 (v2 in examples) | v7 |
| `actions/upload-artifact` | `.github/workflows/validate-template.yml`, examples | v4 | v7 |
| `actions/setup-dotnet` | skill examples | v2 | v5 |
| CI Python | `validate-template.yml` | 3.11 | 3.14 |
| `PyYAML` | CI install step, docs | unpinned | 6.0.3 (pinned) |
| `pytest` | CI install step, docs | unpinned | 9.1.1 (pinned) |

Third-party vendored Hugo themes under `.ai/skills/hugo/templates/*/themes/` are
upstream copies and are left untouched.

## Steps

- [x] Add `requirements-dev.txt` pinning PyYAML and pytest
- [x] Refresh action pins and Python version in `.github/workflows/`
- [x] Wire CI and docs to `requirements-dev.txt`
- [x] Refresh action pins and version references in skill examples and docs
- [x] Review the repository read-only for drift, stale references and hygiene
- [x] Run the validation suite and inspect the final diff

## Out of scope

- Updating vendored third-party Hugo themes
- Rewriting validator logic (fixes only, if the review finds defects)
