# Security Agent — Template Addition

**Status:** APPROVED (user instruction: "add the security agent now")
**Slug:** security-agent
**Follows:** `.ai/completed/council-principle.md`

---

## Why

The template ships 8 agents and none of them is security. Three security *skills* exist
(`security` — strategy/compliance/threat modelling, `api-security` — OWASP API Top 10,
`software-security` — secure coding/OWASP/reviews), so a fourth skill would duplicate. What is
missing is an **agent** — a first-class persona that can be seated, delegated to, and routed to.

The council work exposed this concretely: the Security seat is currently `reviewer` briefed with
the `security` skill, and three artifacts assert as fact that **"there is no `security` agent in this
template"**. Adding the agent makes those assertions false, so the roster, the seat tables, and the
chain must be swept in the same change — otherwise the template documents a roster that contradicts
its own agents directory.

## The agent

`.ai/agents/security.md` — ninth agent, deep tier, **read-only by design** (reports, does not fix —
same posture as `reviewer`). Frontmatter schema mirrored from `reviewer.md` / `architect.md`, never
invented; `runAs: subagent` is required by **`validate-reasonix.py:133-145`** (verified during
implementation — *not* `validate-pi.py`, which validates only the `.pi/` junctions and
`.pi/settings.json`).

Wide tool set than `reviewer` by one: `Bash`, so dependency-vulnerability audits and secret scans are
possible, with no `Write`/`Edit` so it cannot silently change what it audits.

Skills: `security`, `api-security`, `software-security` — the three existing skills, no new ones.

## Blast radius (8 files)

| # | File | Change |
|---|---|---|
| 1 | `.ai/agents/security.md` | **CREATE** — the persona |
| 2 | `.ai/reference/council.md` | Seat table: Security → `security` agent (was `reviewer` + skill) |
| 3 | `.ai/skills/council/SKILL.md` | Seat row; replace the "no `security` agent" assertion; rewrite the correlated-persona bullet |
| 4 | `.ai/chains/council.chain.md` | Two blocks `## reviewer` → `## security`; drop "shares your agent name"; update the mandate lines |
| 5 | `README.md` | Agents table row; de-number `### Specialized Agents (8)` |
| 6 | `AGENTS.md` | `/run security "task"` row in the agent table |
| 7 | `TEMPLATE-USAGE.md` | "8 agents with `runAs: subagent`" — de-number |
| 8 | `.github/copilot-instructions.md` | Add only if a natural slot exists (PROJECT_OWNED, local only) |

**Added during implementation — the plan's blast radius missed these two:**
| 9 | `CLAUDE.md` + `DEEPSEEK.md` | The `Agent | Model | Use For` delegation table (`CLAUDE.md:68-77`) drives subagent routing and has no `security` row. Byte-identical edit in both. |
| 10 | `.ai/skills/verify-config/SKILL.md:80` | States "the same 8 agent types as `CLAUDE.md`" — a live doc asserting a count that is now wrong. De-number. |

Both were found by the roster agent, not by the plan. File 9 is the more important miss: the root
documents that actually route subagents could not reach the new agent.

Plus `.ai/reference/work-type-mapping.md` if its table has an agent mapping to update.

## Reused, not duplicated (rule 12)

- The three existing security **skills** — the agent loads them, it does not restate them.
- `.ai/agents/reviewer.md` and `architect.md` as the frontmatter/body templates.
- The council's mandate vocabulary — the Security seat keeps its mandate wording ("blast radius and
  exposure").
- The deep/fast tier convention — `model: sonnet` mirrors how existing deep-tier agents declare it.

## Notes carried from the council work

- The council's residual bullet about two seats sharing one persona (`reviewer` for both Rules and
  Security) was **created by the absence of this agent**. It must be rewritten, not deleted: `reviewer`
  still loads the `security` skill, so some overlap survives even with distinct agents, and claiming
  otherwise would be the same class of overstatement the audit caught.
- Counts are **de-numbered** where a heading states one, exactly as the skills heading was, so they
  cannot drift again (README already said "8" while the tree listed 32 of 37 skills).
- No concrete model names in agent bodies; tiers only.

## Gates

- `.ai/tests/run-all-tests.sh` — 11/11, including `validate-pi.py` on the new agent file.
- `grep -ri "no .security. agent"` across `.ai/` → zero hits (the assertion is gone, not duplicated).
- `diff CLAUDE.md DEEPSEEK.md` → still empty (untouched by this change).
- `hygiene-lint.py` → 0 issues.

No commit unless asked.
