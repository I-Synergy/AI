# Fix Install Documentation

**Status:** DONE
**Started:** 2026-11-08

## Problem

`README.md` and `TEMPLATE-USAGE.md` still present `cp -r ./.ai` (the full catalog —
71 skills, 724 files, ~8.6 MB) as the primary Quick Start. This contradicts the
AI Workspace Manager section in both files, which exists precisely to install a
selection instead of the whole catalog. The docs also never state which
directories are always copied because they are referenced by literal path.

## Decision

Keep the distribution model unchanged (files on disk + junctions + curated
install). Fix the documentation only:

1. Make AI Workspace Manager the primary install path.
2. Demote `cp -r` to a manual/air-gapped fallback.
3. Document the always-copied directories (`reference/`, `patterns/`,
   `checklists/`, `project/`, `scripts/`, `tests/`) and why they cannot be
   selected.
4. Add a drift-check step and state that junctions are local, not committed.

## Files

| File | Change |
|---|---|
| `README.md` | Quick Start: extension-first, manual fallback, always-copied table, drift check, renumbered steps |
| `TEMPLATE-USAGE.md` | Quick Start: extension-first, manual fallback; extension heading `(Optional)` → `(Recommended)` |
| `TEMPLATE-FAQ.md` | Q8 aligned with the extension-first flow; install tip in Quick Start Tips |

## Out of scope

- No MCP server or transport change.
- No change to `sync-platforms.py`, the resolver, or the validation suites.
- No new catalog kinds (reference/patterns remain always-copied).
