# Model Naming Refresh

**Status:** DONE
Started: 2026-09-25
Completed: 2026-09-25

## Steps

- [x] 1. writer: refresh the model mapping in `DEEPSEEK.md`, `README.md`, `.ai/skills/verify-config/SKILL.md`, `powershell/README.md`
- [x] 2. orchestration: run `.ai/tests/run-all-tests.sh` — 11/11
- [x] 3. orchestration: re-stage the refreshed files and commit council + security + refresh
- [x] 4. complete: move progress to `.ai/completed/model-naming-refresh.md`

## Notes

**Trigger:** the DeepSeek backend now ships **one** model. `powershell/Microsoft.PowerShell_profile.ps1`
maps every slot to `deepseek-flash` — the heavy slots (opus/sonnet) request the 1M context window via
the `[1m]` suffix, haiku gets the plain name, and `CLAUDE_CODE_SUBAGENT_MODEL = inherit`. The names
`deepseek-v4-pro`, `deepseek-v4-flash`, and `deepseek-v4-flash-vision-exp` are **dead**; vision is
unified, so the manual-override guidance for `designer`/`ui-developer`/`ui-tester` is obsolete.

**Decision (user, in-session):** *point at the profile* — do not duplicate the mapping. Agent
`model:` frontmatter keeps the tier aliases (`sonnet`/`haiku`); the concrete model per slot is defined
by the backend profile, which is the single source of truth. Rationale: a duplicated mapping goes
stale exactly like the rule count and the agent count did in this repo.

**Blast radius at decision time:** 41 occurrences across 5 files — `CLAUDE.md` (12, removed by the
master restore, must NOT be re-added: the neutral master stays model-free), `DEEPSEEK.md` (12),
`README.md` (10), `powershell/README.md` (4), `.ai/skills/verify-config/SKILL.md` (3).

**Notable:** `verify-config`'s drift check currently *asserts* the dead names, so it would bless
stale files and flag accurate ones. The check inverts: agents must use the tier aliases, and shared
docs must NOT hardcode concrete model names.

**Staging note (revised during execution):** `powershell/README.md` **is** included in the commit.
The plan was to leave it unstaged with the user's profile work, but excluding it would keep a document
in the committed tree that describes a profile which no longer exists anywhere — actively false, and
worse than the mild untidiness of committing a doc a step ahead of the script it documents. The
profile script itself (`powershell/Microsoft.PowerShell_profile.ps1`) remains uncommitted with the
user's in-flight work.
