# Dependency Refresh and Repository Review

Status: DONE
Started: 2026-10-27
Completed: 2026-10-27
Written By: Reasonix Code

## Summary

Refreshed every external dependency the template actually declares and reviewed the
repository. There is no Node.js/npm project, .NET solution or lockfile in this repo —
the dependency surface is GitHub Actions pins, the CI Python version, and two Python
packages used by the validation suite.

## Changes

1. **`requirements-dev.txt` (new)** — pins `PyYAML==6.0.3` and `pytest==9.1.1`; added to
   `TEMPLATE_OWNED` in `.ai/scripts/upgrade-template.py` so upgrades propagate it.
2. **`.github/workflows/validate-template.yml`** — `actions/checkout@v4→v7`,
   `actions/setup-python@v5→v7`, `actions/upload-artifact@v4→v7`, Python `3.11→3.14`,
   installs from `requirements-dev.txt`, and declares `permissions: contents: read`.
3. **`.github/workflows/mirror-to-azure.yml`** — checkout `v4→v7`, `permissions: contents: read`.
4. **Docs** — `README.md`, `.ai/tests/README.md`, `.ai/tests/TESTING-GUIDE.md`,
   `.ai/tests/QUICK-REFERENCE.md`, `TEMPLATE-FAQ.md`, `TEMPLATE-USAGE.md`, `pip.ini` all
   point at `requirements-dev.txt`; Python floor corrected 3.8 → 3.10 (pytest 9 requires
   `>=3.10`); example workflows/GitLab CI moved to Python 3.14.
5. **Skill/template examples** — action pins refreshed: checkout v1/v2/v4→v7,
   setup-dotnet v2→v5, upload-artifact v2/v4→v7, setup-python v2→v7,
   peaceiris/actions-hugo v2→v3, codecov v2→v7, docker setup-buildx/login v1→v4,
   metadata v5→v6, build-push v5→v7, dependency-review v2→v5.

## Review findings

- **Fixed (high):** `pip install --config-file pip.ini` is not a valid pip option
  (`pip --help` has no `--config-file`); it appeared in six files. Replaced with
  `PIP_CONFIG_FILE=pip.ini pip install ...`.
- **Fixed (medium):** `requirements-dev.txt` was absent from `TEMPLATE_OWNED`.
- **Fixed (low):** both workflows lacked explicit least-privilege `permissions`.
- **Fixed (low):** documented Python floor (3.8) contradicted pytest 9's `>=3.10`.
- **Left as-is:** the three vendored Hugo theme workflows still pin `checkout@v4` —
  they are upstream copies under `themes/`.
- **Verified clean:** no committed secrets or build artifacts; all 80 skill dirs have
  `SKILL.md`; README's 80 skill rows + 8 pattern-guide rows match the filesystem;
  stale references to removed validators exist only in `.ai/completed/` and historical
  plans.

## Verification

- `python3 -m pytest .ai/tests/test_suite.py -q` → 13 passed (pytest 9.1.1, Python 3.14.7)
- `bash .ai/tests/validate-references.sh` → 19 passed, 0 failed
- `python3 .ai/tests/validate-upgrade-script.py` → 13/13 passed
- `git diff --check` → clean
