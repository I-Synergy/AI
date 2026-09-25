# Council Principle — Template Addition

**Status:** AWAITING APPROVAL
**Slug:** council-principle
**Requested by:** User — "can we add the principle of a council to this template?"

---

## Decisions Settled With The User

| Question | Answer |
|---|---|
| Council form | **Independent positions → synthesis.** Seats form positions alone, then a chair reconciles them. |
| Trigger | **High-stakes only.** Architecture, public contracts, destructive migrations, security posture, irreversible choices. |
| Verdict weight | **Advisory, dissent recorded.** Chair decides on merits; minority positions written down; unresolved dissent escalates to the user. |
| Deliverable | **Full mechanism.** Principle + reference doc + skill + chain + companion docs + validators. |

---

## The Principle (condensed — the reference doc will expand it)

> A decision that is expensive to reverse is not made by one agent's judgment. It is made by a
> council whose seats form positions **independently**, then reconciled by a chair who **records
> dissent instead of averaging it away**.

Four properties make it a council rather than a panel of redundant reviewers:

1. **Independence first** — seats never see each other's positions or the chair's leaning before
   forming their own. Without this, seats herd toward the first answer they read and the council
   produces one opinion at N× the cost.
2. **Conflicting mandates** — seats are chosen because they will disagree (feasibility vs. rule
   compliance vs. security blast radius vs. verifiability), not because they agree.
3. **Self-objection required** — every seat must return the strongest argument against its own
   position. This kills the polite, unanimous output that makes councils worthless.
4. **Dissent is recorded verbatim** — the chair writes what was rejected and why, plus the
   conditions that would reopen the decision. Averaging is forbidden.

**Anti-patterns the doctrine names explicitly:** seats sharing a context; asking "do you agree?";
averaging positions into mush; convening on everything; the chair voting; using a council to
diffuse responsibility for a decision nobody wants to own.

---

## Artifacts

Owner column uses the template's own agent roster from `.ai/agents/`.

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 1 | `.ai/reference/council.md` | **CREATE** | `architect` | Source of truth for the principle. Triggers, seat selection, protocol, anti-patterns, position-brief + synthesis-record templates, worked example. |
| 2 | `.ai/skills/council/SKILL.md` | **CREATE** | skill author invoking `skill-creator` | Invocable `/council`. Must include a fenced block (see validation gate V4) and a description unique across all skills (hard fail in `smoke-test.py:128-145`). |
| 3 | `.ai/chains/council.chain.md` | **CREATE** | `architect` | pi-only wrapper. Carries an explicit independence caveat — see Risk R1. |
| 4 | `CLAUDE.md` | **EDIT** | `writer` | New `### When to Convene a Council` under `## Task Execution Protocol` (after *When to Plan*), plus a `## Reference Appendix` entry for `.ai/reference/council.md`. Backticked path must resolve (`validate-claude-md.py:179-186`). |
| 5 | `DEEPSEEK.md` | **EDIT** | `writer` | Byte-identical mirror of #4 — required, see Risk R2. Verify with `diff`. |
| 6 | `AGENTS.md` | **EDIT** | `writer` | Chain table row (`:28-32`) — currently the only user-facing chain documentation. |
| 7 | `REASONIX.md` | **EDIT** | `writer` | Short council line in `## Task Execution` + `## Key Reference Files` row. New sections/rows are safe for `validate-reasonix.py:68-85`; the nine required headings must not be renamed. |
| 8 | `.ai/reference/work-type-mapping.md` | **EDIT** | `writer` | Council row — this file, not CLAUDE.md, is where the mapping table actually lives. |
| 9 | `.github/copilot-instructions.md` | **EDIT** | `writer` | `## Work-Type Context Mapping` row (`:173-197`). PROJECT_OWNED → never pushed downstream; local consistency only. |
| 10 | `README.md` | **EDIT** | `writer` | Skills table row, Work-Type Context Mapping row, File Structure tree. De-number the `### Specialized Skills (35)` heading — the count is already wrong (36 actual) and will drift again. |
| 11 | `TEMPLATE-USAGE.md` | **EDIT** | `writer` | `:142` skills count, `:144` "Chain definitions (2 chains)" → 3. Prefer de-numbering. |
| 12 | `.ai/scripts/upgrade-template.py` | **EDIT** | `developer` | **Required:** add `.ai/reference/council.md` to `TEMPLATE_OWNED` (`:36-59`). `.ai/reference` is not directory-owned, so without this the doc never reaches downstream projects. `validate-upgrade-script.py:236-263` checks ownership completeness. |
| 13 | `.ai/checklists/pre-submission.md` | **EDIT** | `writer` | New `## Council Gate (High-Stakes Decisions)` section of checkboxes. Nothing validates its contents; existence only. |
| 14 | `.ai/tests/validate-structure.sh` | **EDIT** | `developer` | *Hardening:* add `council.md` to the hardcoded `reference_files` list (`:88-94`). Currently no coverage. |
| 15 | `.ai/tests/validate-settings.py` | **EDIT** | `developer` | *Hardening:* add `.ai/chains` to required dirs (`:140-151`). Currently unchecked. |

### Explicitly reused (rule 12 analogue — no new duplicates)

- **`.ai/agents/*`** — seats are drawn from the existing 8 agents. No new agents are created.
- **`.ai/plans/` + `.ai/progress/`** — the council's framing and synthesis records use the existing
  plan/progress mechanism. No new record format, no new directory.
- **The escalation path** in `.ai/reference/task-execution.md` — unresolved dissent reuses it.
- **`skill-creator`** — the skill is authored through the existing skill-authoring path.
- **Existing chain format** — `## agent` / `phase:` / `label:` / `reads:`, no schema extension.

---

## Sequencing

```
Step 1  architect ──► .ai/reference/council.md          (everything else derives from this)
        │
Step 2  ├── skill author (skill-creator) ──► .ai/skills/council/SKILL.md
        ├── architect ──► .ai/chains/council.chain.md
        └── writer ──► artifacts 4-11, 13            (all read council.md)
        │
Step 3  developer ──► artifacts 12, 14, 15            (independent of 2)
        │
Step 4  orchestration ──► run .ai/tests/run-all-tests.sh, read output
        │
Step 5  reviewer ──► audit the whole change set
        │
Step 6  progress file ──► .ai/completed/council-principle.md
```

Step 1 must land before Step 2 — every other artifact cites the principle, and authoring them in
parallel against an unwritten source of truth is how the mirrors drift.

---

## Validation Gates

| Gate | Command | Must hold |
|---|---|---|
| V1 | `.ai/tests/run-all-tests.sh` | All 11 suites pass (pre-runs `sync-skills.py`) |
| V2 | `validate-claude-md.py` | Backticked `.ai/reference/council.md` + `.ai/skills/council/SKILL.md` resolve; no new warnings |
| V3 | `diff CLAUDE.md DEEPSEEK.md` | Empty (Risk R2) |
| V4 | `smoke-test.py` | Council description is unique; `allowed-tools` is a YAML list from the known set |
| V5 | `validate-references.sh` | Any markdown link to council docs in CLAUDE.md/README.md resolves on disk |
| V6 | `validate-upgrade-script.py` | Passes with the new TEMPLATE_OWNED entry |

`dotnet build`/`dotnet test` do not apply — this change touches no C#. The Python/shell validators
are the analogue and are the gate.

---

## Risks & Honest Limitations

**R1 — The pi chain cannot guarantee independence.** Chains are a linear pipeline with `reads:`,
and `implement-and-review.chain.md:15-25` shows a step receiving prior context even with no explicit
`reads:`. If the pi runner shares a conversation across steps, seat 2 sees seat 1's answer and the
council degrades into a panel — exactly the anti-pattern. No runner code exists in this repo to
verify the semantics (no validator even opens a `.chain.md`). **Handling:** the chain file carries an
explicit caveat — if your runner shares context between steps, invoke each seat as a separate run
instead. The chain is shipped as a convenience with its limitation stated, not as a silent
violation of the principle. Flagged for the reviewer to confirm or correct.

**R2 — `DEEPSEEK.md` silently overwrites `CLAUDE.md`.** `powershell/Microsoft.PowerShell_profile.ps1:30-46`
copies `DEEPSEEK.md` → `CLAUDE.md` at session start for the DeepSeek backend, and the two files are
byte-identical today. A council section added to CLAUDE.md but not DEEPSEEK.md is **erased** on that
backend. `verify-config/SKILL.md:70` already records this as a known silent-drift gap. Both files ship
in the same commit; gate V3 proves it.

**R3 — Do not add a 14th critical rule.** `.ai/chains/implement-and-review.chain.md:21` hardcodes
"all 13 rules", and the 13 are all *coding* rules ("violating any of them causes bugs"). The council
is a decision *process*, so it belongs under Task Execution Protocol. Placement avoids the coupling
rather than requiring a fix to a chain file.

**R4 — `.ai/session-context.md` will NOT be written.** The template's own end-of-session protocol says
to write a handoff there, but in *this* repo that file is the shipped, unfilled `CUSTOMIZE THIS`
placeholder — writing project state into it would corrupt the template for every downstream project.
The record goes to the progress file → `.ai/completed/` instead. **Deviating from a template rule
deliberately; calling it out for your approval.**

---

## Out Of Scope (pre-existing drift, not caused by this change)

Recon surfaced stale counts well beyond this task. Fixing them here would bury the council diff:

- `README.md:13` says 35 skills; 36 exist (`mobile-release` missing from the table)
- `.ai/tests/README.md:21` "15 skill directories"; `TESTING-GUIDE.md` and `QUICK-REFERENCE.md` similar
- `.pi/CONVERSION-SUMMARY.md` "15 skills"; `.pi/SKILLS-README.md` 25-row table
- Suite counts disagree across `TEMPLATE-FAQ.md` (10) vs `README.md` (11)
- `validate-claude-md.py:218,239` reference a "Work-Type Context Mapping section" that does not exist
  in CLAUDE.md — a stale validator message

Recommend a separate cleanup pass. Only the counts our change touches get fixed now, and where
possible by de-numbering rather than re-numbering, so they cannot drift again.

---

## Open Items For The Reviewer

1. Does the chain caveat (R1) state the limitation accurately, or can independence be expressed in
   the chain format after all?
2. Is the high-stakes trigger list tight enough to resist mission creep, and does any trigger
   overlap or conflict with an existing rule?
3. Do the four companion docs (CLAUDE/DEEPSEEK/REASONIX/copilot) stay consistent with each other and
   with `council.md`, given each has a different structure?
4. Does the council duplicate anything already provided by `design-interrogation`, `gap-review`, or
   `code-reviewer`, such that one should be delegating to the other instead?

---

## Approval

No files are created or edited until you approve this plan. On approval I will create
`.ai/progress/council-principle.md` and start at Step 1. No commit will be made unless you ask.
