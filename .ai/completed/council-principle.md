# Council Principle

**Status:** DONE
Started: 2026-09-25
Completed: 2026-09-25

## Steps

- [x] 1. architect: author `.ai/reference/council.md` (source of truth)
- [x] 2. skill author via skill-creator: `.ai/skills/council/SKILL.md`
- [x] 3. architect: `.ai/chains/council.chain.md` (pi wrapper + independence caveat)
- [x] 4. writer: CLAUDE.md council subsection + Reference Appendix entry
- [x] 5. writer: mirror CLAUDE.md section into DEEPSEEK.md (byte-identical)
- [x] 6a. writer: AGENTS.md chain table + REASONIX.md (instruction docs)
- [x] 6b. writer: `.ai/reference/work-type-mapping.md` + copilot Work-Type table
- [x] 7. writer: README.md + TEMPLATE-USAGE.md + pre-submission.md council gate
- [x] 8. developer: upgrade-template.py TEMPLATE_OWNED + validate-structure.sh + validate-settings.py
- [x] 9. orchestration: run `.ai/tests/run-all-tests.sh` — all 11 suites pass
- [x] 10. verify `diff CLAUDE.md DEEPSEEK.md` is empty
- [x] 11. reviewer: audit the full change set (1 blocking, 12 non-blocking findings)
- [x] 11a. fix pass: chain (F1/F2/F3/F12) · reference+skill (F4/F6–F9/F11) · companions (F4/F5/F6/F10)
- [x] 11b. reviewer: verify each fix landed, no new inconsistency, re-run suite
- [x] 11c. fix pass 2 (verification findings): chain N1 + digest phase label · reference+skill N2/N3/N4 + no-spawn fallback · companions N2 propagation · re-run suite
- [x] 12. complete: move progress to `.ai/completed/council-principle.md`

## Notes

Plan: `.ai/plans/council-principle.md` (approved 2026-09-25).

Semantics approved by user: independent positions → synthesis · high-stakes triggers only ·
advisory verdict with dissent recorded · full mechanism.

Deliberate deviations, approved:
- Council is NOT critical rule 14 (it is a process, not a coding rule). Lives under Task Execution
  Protocol. Avoids breaking `implement-and-review.chain.md:21` ("all 13 rules").
- `.ai/session-context.md` is NOT written — in this repo it is the shipped CUSTOMIZE-THIS
  placeholder. Record goes here instead.
- `.ai/reference/council.md` MUST be added to TEMPLATE_OWNED (`.ai/reference` is not dir-owned).

Known risks: chain cannot guarantee seat independence (caveat shipped in-file).

Corrections made after the Step 11 audit:
- The DeepSeek PowerShell profile does NOT persistently overwrite CLAUDE.md. It copies `DEEPSEEK.md`
  over it and restores the original in a `finally` block. Both files still ship together so the
  council section survives the swap either way — the mitigation stands, the plan's wording was wrong.
- The plan's evidence for the chain context-bleed risk was mis-cited: `implement-and-review.chain.md:15-25`
  DOES declare `reads:` at :18. The steps that inherit context without declaring it are in
  `scout-plan-implement.chain.md:22-52`. The conclusion held; the evidence did not.

Deferred to a follow-up bundle (NOT part of this change):
- **DONE 2026-09-25** (see `.ai/completed/security-agent.md`) — Security agent (9th), harmonising
  `council.md` seat table, `SKILL.md:133`, and the chain's two `reviewer` seats; plus roster updates
  in README/AGENTS/copilot/TEMPLATE-USAGE. The real blast radius was wider than this list: the
  `CLAUDE.md`/`DEEPSEEK.md` delegation table and `.ai/skills/verify-config/SKILL.md:80` also carried
  the agent count and needed the same sweep.
- `.ai/reference/aot-and-trimming.md` missing from TEMPLATE_OWNED (same class of bug we fixed here).
- `implement-and-review.chain.md:21` stale "all 13 rules" (`.ai/reference/critical-rules.md` has 26).
- AGENTS.md and DEEPSEEK.md are in neither TEMPLATE_OWNED nor PROJECT_OWNED — needs an ownership
  policy decision, not a mechanical fix.
- skill-creator's eval loop was skipped for `council` (the brief constrained the agent to one file).
- Pre-existing stale counts: README skills table missing `mobile-release`; README tree lists 32 of 37
  skills; `TEMPLATE-USAGE.md:261` says 10 suites.
