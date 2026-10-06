# Agentty skill-lint findings — triage and fixes

**Status:** DONE
Completed: 2026-10-04
Trigger: eight findings reported from the agentty **Ctrl+K → Skills panel** across seven skills.

## Where these findings come from

They are **not** from `agentty skills`. That CLI verb runs spec lint only (name/description/body
≤ 500 lines) and reports `N skill(s), M warning(s)`. Running it against this repo showed the 37
project skills clean; its only warnings were `name does not match parent directory` on user-level
skills.

The four messages come from agentty's **skill-body screener** (`screen_body()` in
`src/tool/skills_screen.cpp`), rendered in two surfaces:

1. the **Ctrl+K → Skills panel** (read-only; rows worst-first), and
2. the **consent screen** of `agentty skill add` / `agentty skill approve`.

It reads **only the SKILL.md body** — frontmatter is never screened and `references/` is never
scanned — and the line number is body-relative, counted as *file line − (closing `---` line + 1)*.

## The rules that fired (verbatim literals, case-insensitive substring matches)

| Code | Level | Trigger |
|---|---|---|
| `hidden-directive` | Critical | a line containing `<!--` **and** any of `instruction`, `ignore`, `secret`, `token`, `do not tell`, `don't tell` |
| `destructive` | Warn | `rm -rf /`, `rm -rf ~`, `git push --force`, `git push -f`, `DROP TABLE`, `mkfs` |
| `conceal-from-user` | Critical | `do not tell the user`, `don't tell the user`, `without informing`, **`silently`**, `without mentioning` |
| `instruction-override` | Critical | `ignore previous instruction`, `ignore all previous`, `disregard the above`, **`developer mode`**, `you are now`, **`system:`**, `security warnings are` |

There is **no negation, allowlist, fence- or comment-awareness anywhere** in the screener. Every
finding below was a substring hit; three of the eight were on lines asserting the opposite.

## Findings and dispositions

| Skill | Text | Code | Disposition |
|---|---|---|---|
| book-to-skill | `<!-- ~2,000 tokens: … -->` | hidden-directive | **real** — comment converted to visible italic text (the word *tokens* contains `token`) |
| book-to-skill | `rm -rf /tmp/book_skill_work` | destructive | **real** — scoped `rm -f` + `rmdir`; `/tmp` → `.ai/tmp` (repo rule); `rm`/`rmdir` added to `allowed-tools` |
| council | "never **silently** absorbed" | conceal-from-user | false positive (asserts the opposite) — reworded |
| design-interrogation | "Never **silently** skip." | conceal-from-user | false positive — reworded |
| upgrade-template | "**Silently** skipped." | conceal-from-user | false positive — reworded |
| verify-config | "go stale **silently**" | conceal-from-user | false positive — reworded |
| skill-creator | "three-level loading **system:**", "**filesystem:**" | instruction-override | false positive on the bare `system:` literal — reworded to "loading model" / "on disk" |
| winui-specialist | "**Developer Mode** is enabled" | instruction-override | false positive — a Windows setting name — reworded to "Dev Mode" |

Also fixed on its own merits: `skill-creator`'s output-format example used an all-caps `ALWAYS`
while the same file's line 115 tells authors never to write ALWAYS in caps.

Final state: a sweep of every `SKILL.md` body against the four verbatim literal sets returns **0
hits**. `validate-skills.py` 37/37, `validate-structure.sh` 47/47, `hygiene-lint` 0 issues.

## Consequences worth knowing

- **User-scope copies keep flagging.** The panel also scans user-level skills, and stale synced
  copies under `~/.claude/skills/synced/…` still contain `silently` (morning, pptx,
  google-workspace, computer-use) and `~/.agents/skills/…` swept clean. A non-zero flag count after
  this work is expected until those copies change; they are outside this repo.
- **`update-skills` carries a `dynamic-context` Note** for the `` !` `` sequence in its body. That is
  the intended Claude Code syntax — agentty does not execute it. Left as is.
- **The screener is pattern matching, not proof.** Rewording to satisfy it is cheap here because the
  substitutes read at least as well, but two of the eight fixes were pure linter appeasement of
  correct prose. Worth reporting upstream.

## Work delivered alongside this triage

- `.ai/skills/book-to-skill/scripts/extract.py` — the extractor the skill referenced but which had
  never existed. Stdlib-only; EPUB via zipfile/html.parser, PDF via `pdftotext`; writes
  `.ai/tmp/book_skill_work/{full_text.txt,metadata.json}` with `chapters` character offsets.
- `.ai/commands/` — 37 slash-command files (one per skill, flat, named exactly after the skill),
  junctioned into **both** `.claude/commands` and `.agentty/commands`, wired into `sync-skills.py`
  and `.gitignore`. `argument-hint` uses a plain scalar (`<task or question>`) — a bracketed value
  parses as a YAML list.
- `.ai/reference/agentty-environment.md` — the size-bounding environment variables, which cannot be
  declared in any config file, plus the fact that context window is set with Ctrl+W in the model
  picker rather than by variable.

## Not done

Nothing was installed or approved via `agentty skill add` — verification used source-derived literal
sweeps rather than the panel, to avoid a state change in `~/.agentty`. Confirming in the Ctrl+K panel
(reopen it; rows recompute on open) is the user's call.
