# Security Agent

**Status:** DONE
Started: 2026-09-25
Completed: 2026-09-25

## Steps

- [x] 1. writer: create `.ai/agents/security.md` (ninth agent, deep tier, read-only + Bash)
- [x] 2. architect: harmonise the three council artifacts to seat the new agent
      (`.ai/reference/council.md` seat table · `SKILL.md` assertion + seat row + correlated-persona bullet · chain's two `## reviewer` Security blocks)
- [x] 3. writer: roster propagation (`README.md`, `AGENTS.md`, `TEMPLATE-USAGE.md`, copilot doc, work-type mapping) — de-number counts
- [x] 4. orchestration: run `.ai/tests/run-all-tests.sh` — 11/11
- [x] 5. orchestration: grep sweep — no "no security agent" assertion survives anywhere
- [x] 6. complete: move progress to `.ai/completed/security-agent.md`

## Notes

Plan: `.ai/plans/security-agent.md`.

Three artifacts currently assert "there is no `security` agent in this template" as fact
(`.ai/skills/council/SKILL.md:133`, and the seat tables it disagrees with). Adding the agent makes
that false — the sweep in step 2 is mandatory, not cosmetic.

The council's correlated-persona bullet (added by audit finding F9) exists *because* this agent was
absent. Rewrite it accurately: `reviewer` still loads the `security` skill, so residual overlap
survives even with distinct agents.

Pre-existing drift NOT in scope: `aot-and-trimming.md` missing from TEMPLATE_OWNED,
`implement-and-review.chain.md:21` stale rule count, README skills table/tree omissions,
`TEMPLATE-USAGE.md:261` suite count, AGENTS.md/DEEPSEEK.md ownership policy.
