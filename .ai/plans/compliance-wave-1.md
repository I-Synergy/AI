# Compliance Wave 1 — Template Addition

**Status:** APPROVED 2026-09-25 — executing. Progress: `.ai/progress/compliance-wave-1.md`
**Slug:** compliance-wave-1
**Requested by:** User — "Which norms can we add to this template to make the outcome compliant?" → "draft the Wave 1 plan" → "I want that if we run verify-config the repo get all the certifications applied in the readme doc of the repo (not this repo of course)" → "keep it honest … as long as it gives a true view of compatible ISO certifications"

---

## Decisions Settled With The User

| Question | Answer |
|---|---|
| Wave 1 scope | **Three items.** ISO/IEC 25010 as the review rubric, ISO/IEC/IEEE 29119-3 test documentation, and a traceability validator. Waves 2–3 deferred. |
| Standards surface | **Fourth deliverable, and it gets its own file.** `verify-config` generates a standards-compatibility view for the *downstream* project — not this repo, which ships as a template. |
| Claim wording | **Settled: honest only.** Status is *computed from validator exit codes*, never authored. Vocabulary is `Evidence / Aligned / Organizational`. Nothing anywhere says "certified" or "compliant". |
| Placement | **Delegated to me, with the constraint of a true view.** Resolved as two surfaces — `COMPLIANCE.md` (thorough, generated, project-owned) + a short README section pointing at it. Reasoning below. |
| Contract weight | **Additive only.** No new entry in `critical-rules.md`, no change to the 13 rules. Wave 1 adds artifacts and amends skill/agent prose; it does not bind downstream projects to new hard rules. |
| Council | **Does not convene.** Additive and backward-compatible: no documented rule changes, no public contract breaks, no security-posture change. See Risk R6 for the boundary. |

---

## The Problem Wave 1 Actually Solves

The template already has a design → story → slice → test chain. Every link in it is
**by human-readable name**:

| Link | Carried by | Machine-checkable? |
|---|---|---|
| Story → acceptance criteria | `US-{N}` title, then bare `- [ ]` checkboxes | **No** — criteria have no identifier at all |
| Criteria → Gherkin | scenario *name* is free text (`{Criterion 1 scenario}`) | **No** |
| Use case → Gherkin | `AF-1` label exists but is never propagated into Gherkin | **No** |
| Slice → story/usecase | `source: {use_case, user_story}` in blueprint JSON | **Partly** — the only real link today |
| Slice → acceptance criteria | `acceptance_criteria: ["Given … When … Then …"]` — unlabelled strings | **No** |
| Test → criteria | `solution-generator/SKILL.md:41` says "traced to acceptance criteria"; no mechanism, no token in generated code | **No** |

A repo-wide grep for `@SC-|@US-|@UC-|AC-[0-9]|SC-[0-9]|Scenario Outline|Tags:` across
`.ai/**/*.{md,txt,feature}` returns **zero** traceability-shaped hits. Both templates
(`test-class.cs.txt`, `feature-file.feature.txt`) carry only a file-path comment — no
`[TestCategory]`, no `@tag`, no `// Traces:` line.

**So the traceability validator cannot be built on what exists.** Wave 1 must introduce the
identifier convention first. Everything else in this plan depends on Step 1.

---

## The True View

This is the thesis of the whole plan, and it is what `COMPLIANCE.md` will say in a downstream
project. Three values, no fourth:

| Compatibility | Means | Audit value |
|---|---|---|
| **Evidence** | The repo generates an artifact a certification auditor samples directly | Followable to a file |
| **Aligned** | Engineering practice follows the standard's model, but no audit artifact is produced here | Structural, not evidential |
| **Organizational** | Certifiable only at organization level; this repo supplies nothing for it | Named, not claimed |

| Standard | After Wave 1 | What the repo provides | What stays organizational |
|---|---|---|---|
| ISO/IEC 25010 | **Aligned** | Review vocabulary; NFR capture by quality characteristic | — |
| ISO/IEC/IEEE 29119-3 | **Evidence** | Test plan, generated case spec, completion report, incident report | Organizational test policy (Clause 6 / Annexes C–D) |
| ISO/IEC/IEEE 12207 | **Aligned** *(Wave 2)* | Lifecycle process map onto plans / progress / gap-review | — |
| ISO/IEC 27034 | **Evidence** *(Wave 2)* | Per-solution appsec profile + control library | — |
| ISO/IEC 27001 | **Organizational** (partial evidence) | Annex A technological slice: secret scan, dependency audit, config mgmt via git | ISMS, management review, internal audit, risk register |
| ISO/IEC 27701 / 27017 / 27018 | **Organizational** *(Wave 3)* | PII redaction, classification, retention as code | Privacy programme, DPIA governance |
| ISO/IEC 90003 | **Organizational** *(Wave 2)* | Design I/O = plans + interrogation; config mgmt | The QMS it is guidance for |
| ISO 9001 | **Organizational** | Nothing | Entire QMS |
| ISO/IEC 15504 / 33001 | **Organizational** | Process evidence trail (`.ai/progress` → `.ai/completed`) | The assessment itself |
| IEC 62304 | **Organizational** | SOUP inventory ≈ SBOM, if built | Domain QMS, risk file, classification |
| ISO/IEC 42001 | **Organizational** | Nothing yet | The AIMS — and note this repo *is* an AI system |

**The scale is the roadmap.** A standard moves right-to-left as the template grows evidence for
it: Wave 1 moves 25010 from Organizational to Aligned and 29119-3 from Organizational to
Evidence. That is the honest sentence to put in front of a buyer — and it is more persuasive
than a badge, because every "Evidence" cell resolves to a file they can open.

**Why `COMPLIANCE.md` and not README alone.** You asked for the README; the depth belongs in a
file the README points to:

- Procurement and audit reviewers **look for that filename**. It is a known artifact class.
- A 11-row evidence matrix **does not belong in someone's project README**, which is their own
  narrative — stuffing it there gets it deleted, and then there is no true view at all.
- It is **regenerable independently** of the project's README prose, so a regeneration can never
  collide with the user's own edits to their own document.
- The README still gets a short `## Standards Compatibility` section — the entry point, with
  markers so it regenerates idempotently — because the README is what humans read first.

---

## Artifacts

Owner column uses the template's own roster from `.ai/agents/`.

### Step 1 — Identifier convention (the foundation)

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 1 | `.ai/reference/traceability.md` | **CREATE** | `architect` | Source of truth for the scheme. Format, scoping rules, legacy policy, worked example. |
| 2 | `.ai/skills/user-story/SKILL.md` | **EDIT** | `writer` | AC list gains IDs; Gherkin scenarios gain `@AC-…` tags. Output format at `:18-39`; finalization step 3 at `:70` is prose-only today. |
| 3 | `.ai/skills/usecase-specification/SKILL.md` | **EDIT** | `writer` | `UC-{BC}-{NNN}` / `AF-{BC}-{NNN}.{n}`; propagate the AF label into Gherkin. Format at `:18-42`; step 3 at `:73`. |
| 4 | `.ai/skills/vertical-slices/SKILL.md` | **EDIT** | `writer` | `source` (`:31-59`) gains `acceptance_criteria: ["AC-…"]` as **IDs**; `source` becomes array-form where one slice serves several stories. |
| 5 | `.ai/skills/solution-generator/SKILL.md` | **EDIT** | `writer` | Step 7 (`:41`) gets the mechanism it currently only claims: `[TestCategory("AC-…")]` on generated methods. |
| 6 | `.ai/reference/templates/test-class.cs.txt` | **EDIT** | `tester` | Add `[TestCategory("AC-{BC}-{NNN}.{n}")]` + `// Traces: US-… / AC-…` header comment. |
| 7 | `.ai/reference/templates/feature-file.feature.txt` | **EDIT** | `tester` | Add `@AC-{BC}-{NNN}.{n}` tags. |
| 8 | `.ai/patterns/testing-patterns.md` | **EDIT** | `tester` | The feature-file block at `:94-130` is a **verbatim duplicate** of #7 — both must change together or they diverge. Document the tag convention. |

**The scheme** — scoped by bounded context so a bare ID is unambiguous in shared test code:

| Entity | Format | Example | Vehicle |
|---|---|---|---|
| User story | `US-{BC}-{NNN}` | `US-Budget-014` | heading |
| Acceptance criterion | `AC-{BC}-{NNN}.{n}` | `AC-Budget-014.2` | checkbox line |
| Gherkin scenario | `@AC-{BC}-{NNN}.{n}` | `@AC-Budget-014.2` | tag — one per scenario |
| Use case | `UC-{BC}-{NNN}` | `UC-Budget-007` | heading |
| Alternate flow | `AF-{BC}-{NNN}.{n}` | `AF-Budget-007.1` | list item + Gherkin tag |
| Slice | existing `{Entity}.{Operation}` | `Budget.Create` | blueprint `slice` key |
| Test | `[TestCategory("AC-…")]` | `AC-Budget-014.2` | MSTest attribute |

One scenario satisfies exactly one criterion — that constraint is what lets the validator work
in both directions.

**Why scoped rather than bare.** On the evidence, most generated artifacts are *already* scoped by
bounded context through their path — test projects are `{Solution}.{BC}.Tests/`, feature files live
at `docs/slices/{BC}/…`, story files at `docs/bounded-contexts/{BC}/…`. So a bare `AC-014.2` would
resolve unambiguously inside any one of them, and the verbosity buys nothing there.

It buys something the moment artifacts are **aggregated**, and aggregation is precisely what Wave 1
adds: a per-release test completion report spans BCs, and so does the validator's own coverage
output. At that point a bare ID either collides or needs re-scoping at exactly the wrong time.
Scoped IDs are insurance against the aggregation this plan introduces — not against collisions that
exist today. Open Item 1 records the trade for the reviewer.

### Step 2 — Traceability validator

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 9 | `.ai/tests/validate-traceability.py` | **CREATE** | `developer` | Walks `docs/bounded-contexts/**`, `docs/slices/**`, test sources. Checks below. |
| 10 | `.ai/tests/run-all-tests.sh` | **EDIT** | `developer` | **Mandatory.** Discovery is a hardcoded 11-item list (`:47-57`) — no auto-discovery. |
| 11 | `.ai/tests/test_suite.py` | **EDIT** | `developer` | pytest wrapper for Test Explorer (hand-written per suite, 12 functions today). |
| 12 | `.github/workflows/validate-template.yml` | **EDIT** | `developer` | CI hardcodes named steps before calling `run-all-tests.sh`. |
| 13 | `.ai/tests/validate-structure.sh` | **EDIT** | `developer` | *Hardening:* add new reference docs to `reference_files` (`:88-95`). Must-exist list, not exhaustive — optional coverage. |

**Checks** — severity split follows the house style (`validate-claude-md.py` Tests 4–5 are
advisory warnings, not failures):

| # | Check | Severity |
|---|---|---|
| T1 | Duplicate `AC-`/`US-`/`UC-` IDs within a bounded context | **FAIL** |
| T2 | `@AC-` tag in a `.feature` resolves to a declared criterion | **FAIL** |
| T3 | `source.acceptance_criteria` IDs in a blueprint resolve | **FAIL** |
| T4 | `[TestCategory("AC-…")]` resolves to a declared criterion | **FAIL** |
| T5 | Declared criterion has ≥1 scenario | WARN |
| T6 | Declared criterion has ≥1 slice and ≥1 test | WARN |
| T7 | **Legacy mode** — a story file with zero IDs reports one summary warning, not N failures | WARN |

T7 is load-bearing: every already-upgraded downstream project has unlabelled criteria. A hard
fail on day one makes the validator hostile, and a disabled validator is worse than none (R1).

### Step 3 — ISO/IEC 25010 quality model

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 14 | `.ai/reference/quality-model.md` | **CREATE** | `architect` | The nine characteristics (2023 ed.), what each means *for this stack*, the review question per characteristic, and an explicit "measurement is out of scope — that is 25023, evaluation is 25040" boundary. |
| 15 | `.ai/agents/reviewer.md` | **EDIT** | `architect` | The entire review standard is one paragraph at `:11`. Add characteristic attribution + a severity taxonomy. |
| 16 | `.ai/skills/code-reviewer/SKILL.md` | **EDIT** | `writer` | New `## Quality Characteristics` section mapping the existing Security/Performance checklists to characteristics and naming the **missing** ones — interaction capability, reliability, flexibility, safety. **Also fixes the `RemoveItemAsync` drift at `:54`** (R7). |
| 17 | `.ai/skills/design-interrogation/SKILL.md` | **EDIT** | `architect` | Dimension 7 "Non-Functionals" (`:195-204`) is one prose row with no sub-questions. Give it a question set derived from the characteristics. **Highest-leverage 25010 change** — this is where quality attributes *enter* a project, not where they are reviewed. |
| 18 | `.ai/checklists/pre-submission.md` | **EDIT** | `writer` | New `## Quality Characteristics` gate section. |

**Design constraint — do not break the reviewer.** `.ai/agents/reviewer.md` is 11 lines and its
whole philosophy is "Report only high-confidence issues — do not flag style preferences or minor
nits." The rubric adds **attribution and severity, never volume**. Turning a high-signal reviewer
into a checklist generator is the failure mode (R3).

### Step 4 — ISO/IEC/IEEE 29119-3 test documentation (right-sized)

The standard defines **16 information items** across three tiers — counted during execution as
Clause 6: 2, Clause 7: 3, Clause 8: 11. This plan originally asserted 17 without enumerating them;
the executing agent declined to invent a seventeenth row to reach that total and recorded the
discrepancy in the document instead. Adopting all 16 is the documented "Stop 29119" critique —
over-documentation nobody reads. Wave 1 adopts **four**:

The omissions below are this template's own right-sizing decisions, **not** claims about what the
standard permits. Annex A conformance levels (*shall / should / may*) are deliberately **not cited**:
`test-documentation.md` cannot source them, and asserting them would be exactly the unbacked claim
this wave exists to prevent.

| 29119-3 item | Clause | Wave 1 | Why |
|---|---|---|---|
| Test plan | 7.2 / Annex E | **Adopt** — per vertical slice | Derived from the slice blueprint; its entry/exit criteria are what T5/T6 measure against |
| Test case specification | 8.3 / Annex I | **Adopt as generated output** | The AC ↔ scenario ↔ test mapping *is* this document, produced free by Step 1 |
| Test completion report | 7.4 / Annex G | **Adopt** — per release | Carries **residual risks** and **test measures** — the sections an auditor actually samples |
| Test incident report | 8.11 / Annex R | **Adopt** — one per failure | Derivable from MSTest `.trx`; includes the standard's status lifecycle |
| Test policy, org test strategy | 6 / Annexes C–D | **Deferred** | Organizational, not project-level — named in `COMPLIANCE.md` instead |

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 19 | `.ai/reference/test-documentation.md` | **CREATE** | `tester` | Clause → template artifact mapping, **including the 12 omitted items and the reason for each** (organizational, carried by an existing artifact, or no consumer). |
| 20 | `.ai/reference/templates/test-plan.md.txt` | **CREATE** | `tester` | `.ai/reference/templates` is directory-owned — propagates automatically. |
| 21 | `.ai/reference/templates/test-completion-report.md.txt` | **CREATE** | `tester` | |
| 22 | `.ai/reference/templates/test-incident-report.md.txt` | **CREATE** | `tester` | |
| 23 | `.ai/skills/unit-tester/SKILL.md` | **EDIT** | `tester` | Wire plan/report into the completion checklist (`:106-115` — 8 code-only items today). |
| 24 | `.ai/skills/playwright-tester/SKILL.md` | **EDIT** | `tester` | Same, for the E2E surface. |

### Step 5 — Standards-compatibility surface (the honest view)

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 25 | `.ai/reference/standards.md` | **CREATE** | `architect` | The **manifest** — the compatibility table above, machine-adjacent. Per standard: value, implementing artifact, proving validator, organizational remainder. Single source of truth so no surface can drift from reality. |
| 26 | `.ai/reference/templates/compliance.md.txt` | **CREATE** | `writer` | Template for the generated downstream `COMPLIANCE.md`, including the **"what this is not"** statement (R5). |
| 27 | `.ai/reference/templates/standards-section.md.txt` | **CREATE** | `writer` | The short README section, wrapped in `<!-- BEGIN standards-status -->` / `<!-- END standards-status -->`. |
| 28 | `.ai/skills/verify-config/SKILL.md` | **EDIT** | `writer` | New step 6. **Preserves the existing contract at `:102`** — *"Wait for user approval before making changes"*: compute status from validator runs, show the diff for both surfaces, write on approval. Never a silent mutator. |
| 29 | `.ai/tests/validate-standards.py` | **CREATE** | `developer` | `COMPLIANCE.md` exists when generated; markers balanced in both surfaces; every claim resolves to a manifest entry; provenance line present. **This is what makes the view honest by construction** — status is derived from exit codes, so no surface can over-claim. |
| 30 | `.ai/tests/run-all-tests.sh` | **EDIT** | `developer` | Second new suite. |
| 31 | `.ai/tests/test_suite.py` | **EDIT** | `developer` | |
| 32 | `.github/workflows/validate-template.yml` | **EDIT** | `developer` | |
| 33 | `.ai/scripts/upgrade-template.py` | **EDIT** | `developer` | **Required, and the easiest thing to forget.** `.ai/reference` is *not* directory-owned — `.ai/reference/templates` is. Four new reference docs (`traceability.md`, `quality-model.md`, `test-documentation.md`, `standards.md`) must each be added to `TEMPLATE_OWNED` (`:36-61`) **by name** or they never reach a downstream project. Also add **`COMPLIANCE.md` to `PROJECT_OWNED`** so no future template change can stomp a generated per-project view. `validate-upgrade-script.py:236-263` checks completeness. |

**No-op in this repo.** `verify-config` running in the template finds no manifest entries
applicable to a template (as opposed to a generated solution) and writes nothing. That is how
"not this repo of course" is satisfied structurally rather than by a guard.

### Step 6 — Propagation

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 34 | `.ai/reference/work-type-mapping.md` | **EDIT** | `writer` | Rows for the amended task types. `validate-claude-md.py` Test 4 reports unreferenced skills as orphan warnings. |
| 35 | `README.md` | **EDIT** | `writer` | Skills/Pattern Guides tables, the **File Structure tree lists every skill and test script individually** (`:193-345`), new reference docs, and a capability row for the standards surface. `readme-maintenance.md` makes this non-negotiable in the same session. |
| 36 | `CLAUDE.md` | **EDIT** | `writer` | Reference Appendix rows + the reviewer rubric line in the delegation table. Backticked paths must resolve (`validate-claude-md.py:179-186`). |
| 37 | `DEEPSEEK.md` | **EDIT** | `writer` | **Same structural change.** See R2 — this is not a mirror file, it is the file that overwrites `CLAUDE.md`. |
| 38 | `.ai/tests/validate-deepseek-parity.py` | **CREATE** | `developer` | *Hardening, optional.* Nothing verifies parity today; it has caused silent erasure before. Asserts each new section heading is present in both — **not** byte equality (R2). |

### Step 6b — Same-defect cleanup (found during execution, not in the original scope)

R7 folded in **one** instance of the forbidden extension-method pattern. Execution found **three
more**, all outside the five files Step 3 owned. `dotnet-engineer` is the significant one: it is the
primary C# implementation skill, loaded for every .NET and CQRS task, so a solution built by
following it violates `CLAUDE.md` rule 2 on every delete path.

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 39 | `.ai/skills/dotnet-engineer/SKILL.md` | **EDIT** | `writer` | `:50` `RemoveItemAsync<TEntity, TKey>()` and `:54` "use DataContext extensions" both mandate the banned pattern. Replace with the EF Core primitives (mirror `.ai/checklists/pre-submission.md:60`). Check the surrounding section for further instances. |
| 40 | `.ai/skills/api-security/SKILL.md` | **EDIT** | `writer` | `:233` working sample calls `GetItemByIdAsync<...>`. A sample that runs is stronger teaching than prose that forbids — fix the code, not just the sentence. |
| 41 | `.ai/skills/technical-writer/SKILL.md` | **EDIT** | `writer` | `:161` Mermaid label `Handler->>DataContext: AddItemAsync()`. Cosmetic, but it is the same defect and a diagram is copied as readily as code. |

Deliberately **not** included: `critical-rules.md:53-54,105-106` and `cqrs-patterns.md:505-509,663-665`
are counter-examples inside "WRONG / not used" blocks, and `pre-submission.md:59` is a negative list.
Those are correct as written — the defect is mandating the pattern, not naming it.

### Step 5b — Validator regression fixture (accepted during execution)

Neither Wave 1 validator is permanently exercised by CI. This template ships no `docs/` tree, no
`.cs` and no `.feature` files, so `validate-traceability.py` only ever runs against the empty-repo
path in the repository that owns it. It could rot silently — and it is the mechanism the entire
compatibility view rests on, so rot there is invisible until a downstream project hits it.

| # | File | Action | Owner | Notes |
|---|---|---|---|---|
| 42 | `.ai/tests/test_suite.py` | **EDIT** | `developer` | A pytest test that **generates** the fixture into `tmp_path` at runtime: no committed artifacts, no new bash suite, no change to `run-all-tests.sh`'s count, and invisible to every other validator. Asserts T1–T4 fire on a planted defect each and stay silent on clean cases. |

The throwaway fixture built during Step 3 proved the checks once. This keeps them proven — which is
what the V9 honesty gate needs, since force-failing the traceability validator is how the
compatibility view's causation gets tested, and there is no way to force-fail an untested validator.

### Explicitly reused (rule 12 analogue — no new duplicates)

- **The chain itself** — user stories, use cases, slice blueprints, test templates all exist.
  Wave 1 adds identifiers to them; no new artifact type, no new directory.
- **`.ai/reference/templates/`** — directory-owned, auto-propagates; the six new templates need no ownership edit.
- **`.ai/checklists/pre-submission.md`** — the gate mechanism; Wave 1 adds sections, not a new gate file.
- **`verify-config`** — an existing auditor that already reads `README.md` as an audit surface
  (`:50`) and already waits for approval before writing. Extended, not replaced.
- **`.ai/plans/` + `.ai/progress/`** — the record mechanism. No new format.
- **MSTest `[TestCategory]`, Reqnroll `@tags`** — first-class features of mandated frameworks.
  No idiom is introduced that the stack doesn't already have.
- **`validate-claude-md.py`'s advisory-warning pattern** — reused verbatim for T5–T7.

---

## Sequencing

```
Step 1  architect ──► .ai/reference/traceability.md      (nothing else can start first)
        │
Step 2  ├── writer ──► skills 2-5 + pattern 8            (all read traceability.md)
        └── tester ──► templates 6-7
        │
Step 3  developer ──► validate-traceability.py + registration 9-13
        │            └── GATE: run against a fixture; if T1-T4 misfire the scheme is wrong —
        │                fix the scheme, not the validator
Step 4  ├── architect ──► quality-model.md, standards.md, agents 15, 17
        └── tester ──► test-documentation.md + templates 19-24
        │
Step 5  writer ──► verify-config step 6, templates 26-27
        developer ──► validate-standards.py + registration 29-32, ownership 33
        │
Step 6  writer ──► propagation 34-37
        developer ──► hardening 38
        │
Step 7  orchestration ──► .ai/tests/run-all-tests.sh, read output
Step 8  reviewer ──► audit the whole change set
Step 9  progress file ──► .ai/completed/compliance-wave-1.md
```

Step 1 gates everything. Step 3 gates Step 5 — if the ID scheme doesn't survive contact with a
real fixture, the compatibility view has no evidence to compute a status from, and it degrades
into exactly the unbacked claim this plan exists to avoid.

---

## Validation Gates

| Gate | Command | Must hold |
|---|---|---|
| V1 | `.ai/tests/run-all-tests.sh` | **All 14 suites** pass — 11 existing + Traceability, Standards, DeepSeek Parity (pre-runs `sync-skills.py`) |
| V2 | `pytest .ai/tests/test_suite.py` | 16 functions pass — and the audit found **the workflow had no pytest step at all**, so Step 5b's regression fixture was never actually executed by CI. Fixed: the workflow now runs pytest, which is what makes this gate real rather than nominal. |
| V3 | `python .ai/scripts/hygiene-lint.py` | Clean — no stale progress files, no duplicate slugs, no secrets |
| V4 | `validate-claude-md.py` | New backticked reference paths resolve; **no new orphan warnings** |
| V5 | `validate-references.sh` | Every relative Markdown link in `README.md`/`CLAUDE.md` resolves. **Highest-risk mechanical gate** — the crawler at `:100-137` hard-fails on any broken link |
| V6 | `validate-upgrade-script.py` | Passes with the four new `TEMPLATE_OWNED` entries and the `PROJECT_OWNED` addition |
| V7 | `smoke-test.py` | Skill names/descriptions unique across all skills (`:108-145` is a hard fail) |
| V8 | **Structural parity** | Each new section heading present in **both** `CLAUDE.md` and `DEEPSEEK.md`. **Not** byte equality — see R2 |
| V9 | **The honesty gate** | With `validate-traceability.py` force-failed, `validate-standards.py` **must fail** and the generated status must downgrade. If a red validator still yields an "Evidence" claim, the mechanism is broken |
| V10 | Manual | `verify-config` run against this repo writes nothing (no-op assertion, Step 5) |

V9 is the one that matters. Everything else checks that the artifacts exist; V9 checks that the
compatibility view is *caused* by evidence rather than merely permitted to reference it.

`dotnet build` / `dotnet test` do not apply — this change touches no C#. The Python and shell
validators are the analogue and they are the gate.

---

## Risks & Honest Limitations

**R1 — Introducing IDs breaks every already-upgraded project if the validator hard-fails.**
Downstream projects have unlabelled acceptance criteria today. A validator that fails on that
would be disabled within a day, and a disabled validator is worse than none. **Handling:** T7 puts
a story file with zero IDs into legacy mode — one summary warning, never a failure. Legacy mode is
documented in `traceability.md` as a supported state, not a defect.

**R2 — `DEEPSEEK.md` silently overwrites `CLAUDE.md`, and the working tree is swapped *right now*.**
`powershell/Microsoft.PowerShell_profile.ps1:25-50` backs up `CLAUDE.md`, copies `DEEPSEEK.md` over
it, and restores on exit. Live evidence: `git status` shows `M CLAUDE.md`, `md5sum` is identical for
both files, and `CLAUDE.md.deepseek-backup` exists.

**The council plan's gate V3 (`diff CLAUDE.md DEEPSEEK.md` must be empty) is wrong** — it passes
only *while a DeepSeek session is active* and fails everywhere else. At `HEAD` the two files
deliberately differ (different title, identity sentence, and a model-tier paragraph). This plan's V8
asserts the real invariant: **structural parity of new sections**. **Handling:** every root-doc edit
lands in both files in the same commit; when editing `CLAUDE.md`, target the content that survives
the restore, not the swapped-in variant.

**R3 — ISO/IEC 25010 is not a certification and not a checklist.** It is an evaluation model. Two
failure modes: treating it as something to be "certified against", and using it to inflate review
output. **Handling:** `quality-model.md` states the boundary in its first paragraph — it structures
*vocabulary and attribution*, it does not measure. Measurement (25023) and evaluation (25040) are
out of scope, and both are named as such rather than omitted. The rubric adds attribution and
severity only; the finding count of a review must not grow.

**R4 — The 29119-3 documentation set is 17 items and adopting it wholesale produces paperwork.**
**Handling:** four adopted, thirteen omitted *with the reason recorded per item*. The entry criterion
is "does this replace something already needed?" — the test plan is the only genuinely new work; the
test case specification is a free by-product of Step 1.

**R5 — A standards claim in a repo README is worthless to the reader it is aimed at, and a
misrepresentation risk for whoever ships it.** Settled with the user: honest only. **Handling:**
status is computed from validator exit codes, never authored; the vocabulary is
`Evidence / Aligned / Organizational`; gate V9 proves the causation; `COMPLIANCE.md` opens with an
explicit statement of what it is not:

> This document records which engineering artifacts this repository produces and how they relate to
> published standards. **It is not a certification, and nothing here asserts conformity with any
> standard.** Certification is issued by an accredited third-party body after auditing an
> organizational management system. It cannot be established by a code repository, and the
> "Organizational" column names what stays outside this repository's reach.

**R6 — The council boundary, stated so it can be argued with.** Wave 1 adds no rule to
`critical-rules.md`, changes no documented architecture decision, breaks no public contract, and does
not alter the security posture — so no trigger in `.ai/reference/council.md` fires and no council
convenes. **The moment that changes:** promoting any of this into a mandatory critical rule binds
every downstream project that runs `upgrade-template.py`. That *is* a contract change and *does* trip
a trigger. Deliberately deferred to a later wave.

**R7 — Pre-existing drift, and one item folded in on purpose.** The survey found
`.ai/skills/code-reviewer/SKILL.md:54` mandating `RemoveItemAsync<TEntity, TKey>()` — the exact
extension-method pattern that `CLAUDE.md` rule 2, `pre-submission.md:59` and `testing-patterns.md`
forbid. A reviewer skill instructing agents to enforce a banned pattern is actively harmful, and
Step 3 edits that file anyway, so **artifact 16 fixes it**. Everything else in the drift list stays
out of scope (below).

**R8 — `.ai/session-context.md` will NOT be written.** The template's own end-of-session protocol
says to write a handoff there; in *this* repo that file is the shipped `CUSTOMIZE THIS` placeholder,
and writing project state into it corrupts the template for every downstream project. The record
goes to the progress file → `.ai/completed/`.
**Deviating from a template rule deliberately; calling it out for your approval.**

---

## Out Of Scope (pre-existing drift, not caused by this change)

- `README.md:13` "35 skills" vs 36 actual; `.ai/tests/README.md:21` "15 skill directories";
  `TEMPLATE-FAQ.md` (10 suites) vs `README.md` (11) — all stale counts
- `README.md:55` `### Pattern Guides (8)` — a count in a heading, which is why the council plan
  recommended de-numbering rather than re-numbering
- `validate-claude-md.py:218,239` advise editing a "Work-Type Context Mapping section" that does not
  exist in `CLAUDE.md` — a stale validator message
- `AGENTS.md` and `DEEPSEEK.md` appear in **neither** ownership table — an open question carried by
  two prior plans (`council-principle.md:58`, `completed/doc-drift-sweep.md:30`)
- Waves 2–3: 12207 mapping, 27001 Annex A technological controls, 27034, 27701/27017/27018, 42001

---

## Open Items For The Reviewer

1. **Is the bounded-context ID scoping right?** `AC-Budget-014.2` is unambiguous but verbose; bare
   `AC-014.2` is terser but collides across BCs in shared test assemblies. I traded readability for
   unambiguity because the validator needs it — is that the right property to buy?
2. **Does "one scenario satisfies exactly one criterion" hold in practice?** It makes the validator
   trivial. If real stories routinely map N criteria to 1 scenario, the constraint is wrong and the
   tags should be a list.
3. **Is four the right number of 29119-3 items?** Is the test plan genuinely new value, or does the
   slice blueprint already contain it and I am duplicating?
4. **Does the 25010 rubric duplicate `code-reviewer`'s existing Security and Performance checklists**
   to the point where one should delegate to the other instead of both existing?
5. **Does `verify-config` now hold two jobs?** It audits configuration drift *and* generates a
   conformance view. Both read a manifest and both are approval-gated, so they may belong together —
   or the generator may warrant its own skill reading the same `.ai/reference/standards.md`.
6. **AF-derived slices are only half-traced — carried, not fixed.** `vertical-slices` step 3 emits a
   slice per alternate-flow outcome, but `source` has no `AF-` key, so such a slice names its use
   case and not the flow it came from. Adding `alternate_flows: ["AF-…"]` is one line and symmetric
   with the other three keys; it was deliberately **not** added because no Wave 1 check would read
   it — the validator is AC-centric and T1–T7 never touch `AF-`. Same reasoning that rejected the
   `@UC-` tag. Revisit in Wave 2 with the UC-side trace checks, or add the key now if the reviewer
   judges the asymmetry worth closing before anything consumes it.
7. **Use-case main flows have no tag by design** (see Step 1). A scenario carries at most one
   traceability tag — `@AC-` or `@AF-`, never both — so use-case scenarios never enter the AC graph.
   The UC → slice → test path is carried by the blueprint `source` instead. Confirmed coherent in
   review of `.ai/reference/traceability.md:160-164`.

---

## Approval

No files are created or edited until you approve this plan. On approval I will create
`.ai/progress/compliance-wave-1.md` and start at Step 1. No commit will be made unless you ask.

The open questions from the previous draft are resolved: wording is honest-only (R5), placement is
`COMPLIANCE.md` + a README summary, and the ID format is **decided — scoped** (`AC-Budget-014.2`),
on the aggregation reasoning in Step 1.

That last one is the only decision in this plan that is cheap now and expensive later: every
downstream project inherits the format, and changing it after Step 1 means touching every generated
artifact. If you want the terser bare form, say so with your approval and Step 1 changes before
anything is written. Otherwise I proceed with scoped IDs.
