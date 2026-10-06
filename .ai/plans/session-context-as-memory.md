# Plan: Use .ai/session-context.md as memory in every supported CLI client

Status: APPROVED (2026-10-06)
Date: 2026-10-06

## Problem

Every client is told, in prose, to read `.ai/session-context.md` first and write a handoff last
(`AGENTS.md` Session Lifecycle, `.github/copilot-instructions.md` lines ~82-85 and ~200-213,
`.ai/reference/session-management.md`). Nothing loads the file for the client, so it works only
when the model follows the prose. Claude Code can enforce the read; the others cannot be
verified from this repo. The file here is the unfilled template placeholder and must stay so
(user rule: never write project state into it in this template repo).

## Design

| Client | Read at start | Write at end |
|---|---|---|
| Claude Code | `SessionStart` hook prints the file (hook stdout becomes session context), skipped while it is still the placeholder; prose in `AGENTS.md` as backup | prose + handoff template (a hook cannot author a handoff) |
| GitHub Copilot | `.github/copilot-instructions.md` "first action" instruction, worded identically to `AGENTS.md` | same prose |
| Reasonix Code | `AGENTS.md` instruction only (no hook mechanism known to this repo) | same prose |

1. **Hook:** add to the existing `SessionStart` entry in `.claude/settings.json` a second command that
   prints `.ai/session-context.md` when it exists and its first line is not the placeholder
   heading (`# Session Context Template`), preceded by a one-line header, and lists the 5 newest
   files in `.ai/completed/`. Plain `python`/`cat`-style command, no new script, exits 0 always.
   Also run it on `SessionStart` source `compact` so memory survives compaction.
2. **One wording:** a single "Session memory" paragraph, identical in `AGENTS.md` and
   `.github/copilot-instructions.md`: read first; write the handoff (using
   `session-handoff.md.txt`, `Written By` = your client name) before the final reply of any task
   that changed project state; never overwrite another client's entries, append/update sections.
3. **Template-repo exception:** one sentence in the paragraph: in the template repository itself the
   file stays the placeholder; project state goes in `.ai/progress/` and `.ai/completed/`.
4. **Validators:** `validate-settings.py` asserts the hook reads `session-context.md` and skips the
   placeholder; `validate-structure.sh`/`validate-agents-md.py` (or one of them) assert that
   `AGENTS.md` and `.github/copilot-instructions.md` both contain the shared paragraph.
5. **Docs:** `README.md`, `.ai/reference/session-management.md` and `verify-config` describe the
   per-client mechanism truthfully, including that Reasonix/Copilot rely on instructions.

## Decisions (answered 2026-10-06)

1. Every client loads `AGENTS.md` from the repo root; it is the canonical source for the session
   memory wording. `.github/copilot-instructions.md` carries the identical paragraph as a mirror.
2. No Stop-hook enforcement of the end-of-session write; it stays an instruction.

Original questions kept below.

## Open questions (user)

1. Which instruction file does each client actually load now that `CLAUDE.md` is gone? This repo
   assumes `AGENTS.md` for Claude Code and Reasonix and `.github/copilot-instructions.md` for
   Copilot. I cannot verify that from the repo; if Reasonix needs its own file, say so.
2. Should the end-of-session write be enforced for Claude Code with a `Stop` hook that blocks
   while a file in `.ai/progress/` is still `IN PROGRESS`? (Recommended: no. It is intrusive and
   can loop; keep it as prose.)

Council check: adds a hook that only prints project-owned content; no authn/authz, secret or
exposure change, no public contract change. No council.

## Existing files reused

Edit in place: `.claude/settings.json`, `AGENTS.md`, `.github/copilot-instructions.md`,
`.ai/reference/session-management.md`, `.ai/tests/validate-settings.py`,
`.ai/tests/validate-structure.sh`, `README.md`, `.ai/skills/verify-config/SKILL.md`.
No new scripts, no new types.

## Steps

- [x] 1. Resolve open questions 1-2
- [ ] 2. Add the SessionStart (startup, resume, compact) read hook with placeholder skip; test it against the placeholder, a filled file and a missing file in a scratch dir
- [ ] 3. Write the shared "Session memory" paragraph into AGENTS.md and .github/copilot-instructions.md; reconcile session-management.md
- [ ] 4. Validators for hook and paragraph parity
- [ ] 5. Docs and verify-config
- [ ] 6. Verify (pytest, validators, hygiene-lint) and review

## Delegation

`developer`: steps 2, 4. `writer`: steps 3, 5. `reviewer`: step 6. Progress-file Edit
instructions in every prompt.

## Risks

- Hook output is added to every session start: keep it bounded (cap the printed size, e.g. first
  200 lines) so a bloated handoff cannot eat the context window.
- A filled handoff is untrusted text once injected; the header must say it is project notes, not
  instructions.
- Never write into this repo's placeholder while testing; use a scratch directory.
