---
name: product-discovery
description: >
  Plain-language product interview and discovery — capture what to build before designing architecture.
  Produces a product brief, audience profile, UX/UI design briefs, wireframes, mockups, and clickable prototype.
  Use when starting a new product, extending an existing one, or replacing a legacy system.
  Interview the respondent (developer, product owner, or customer) on problem, audience, value, UX, UI, platforms,
  and deliverables. Show wireframes, mockups, and a clickable prototype as you go. Hand off to design-interrogation
  with pre-resolved input so architecture focus stays on technical dimensions only.
  Use when: interview me, new product, product idea, requirements discovery, what should we build, PRD, product brief,
  wireframes or mockups or clickable prototype for a new product.
  Gebruik wanneer: interview mij, nieuw product, productidee, wat moeten we bouwen, ontdekking,
  draadmodellen of mockups of klikbare prototype voor een nieuw product.
---

# Product Discovery

Plain-language interview that captures what you're building: problem, audience, value, UX, UI, platforms, and deliverables.
Produces a product brief, audience profile, design briefs, wireframes, mockups, and a clickable prototype.
Hands off pre-resolved decisions to [`design-interrogation`](../design-interrogation/SKILL.md) so architecture focus stays on technical dimensions.

## What This Skill Does

- **Interviews** the respondent (developer, product owner, or customer) about problem, audience, value, UX, UI, platforms, and deliverables
- **Shows wireframes, mockups, and a clickable prototype** at three fidelity levels; collects reactions as product decisions
- **Produces six discovery documents** plus prototype: product brief, audience profile, UX brief, UI design brief, platform deliverables, decision log
- **Hands off pre-resolved input** to design-interrogation; every `PD-` decision is marked so architecture questions are not re-asked
- **Respondent-aware** — same interview in three modes (developer, product owner, customer); depth and vocabulary adjust, coverage does not

**What it does NOT do:** This skill does not design architecture, select technology stack, or interrogate technical dimensions—that is [`design-interrogation`](../design-interrogation/SKILL.md).

## When to Use

Use when you are starting a new product (greenfield), extending an existing product, or replacing a legacy system. The skill adapts its scope to the product-type fork question: greenfield runs all 18 phases (0–17); extension skips brand/design-system (confirm and amend), and reuses existing UI; replacement adds current-system pain points and migration questions.

Use when the respondent wants to see wireframes, mockups, and a working prototype *during* the interview, not after it closes. Visuals are far more effective than descriptions for getting feedback on information architecture, visual design, and interaction flows. Show-back rounds anchor decisions in reality.

Use when you need a complete product brief that joins **what** the product solves (problem, audience, value, journeys) with **how** it will look and work (UX, UI, platforms, deliverables) in one place. The brief is designed to hand off to [`design-interrogation`](../design-interrogation/SKILL.md) — every decision is pre-resolved so interrogation can focus on technical architecture without re-asking product decisions.

Use when the respondent is not a developer (customer or product owner). Customer mode strips jargon, avoids CQRS and architectural terminology, and flags `[TECH-OPEN]` gaps for the technical colleague to answer later. Customer mode covers **Phases 1–9, 11, 13, and 15** (Problem, Audience, Users, Value, Scope, Market, Journeys, UX, UI, Prototype, Compliance, and Launch); technical phases (Platforms, Data, Operations, Constraints, Risks, Completeness) are deferred or simplified.

## Session Start

Before the first question, check for an earlier session that might have been interrupted:

> I found an earlier session in `docs/product/discovery-decisions.md`. Would you like to **resume** it, **amend** (change some decisions and continue), or **start over**?

**Resume:** reload decisions from the earlier session and continue with open items.  
**Amend:** show which decisions to revise, replay those branches.  
**Start over:** begin fresh (archive the earlier file).

Then load three skills—they are active throughout the session, capturing deliverables as they emerge:

| Skill | Role |
|-------|------|
| `ubiquitous-language` | Capture domain terms as they emerge; draft to file immediately |
| `usecase-specification` | Draft use cases for each bounded context as flows resolve |
| `user-story` | Draft stories as acceptance criteria are agreed |

After loading, ask the respondent's **mode**: Developer / Product Owner / Customer & Business Stakeholder / Mixed. Mode shapes vocabulary and depth, never coverage. Customer mode avoids CQRS and technical jargon, flags `[TECH-OPEN]` gaps for design-interrogation, and covers only the business-facing phases. Developer mode may be terse and reference the codebase directly. Mixed mode asks who is answering which questions.

Then run the **product-type fork** question: **Origin** (new product / extending an existing product / replacing a legacy system) and **Orientation** (internal tool / customer-facing / platform-API; multi-select), as defined in question 0.3 of `references/question-bank.md` to activate skip logic and shape the interview path.

## Mode Coverage Matrix

How respondent mode shapes each phase:

| Phase | Developer | Product Owner | Customer / Business | Notes |
|-------|-----------|---|---|---|
| 0 | ask | ask | ask | All modes answer intake questions |
| 1–2 | ask | ask | ask | Problem and audience are universal |
| 3–4 | ask | ask | simplify (jargon-free) | Personas and value; customer mode avoids technical language |
| 5 | ask | ask | ask | Scope affects all audiences |
| 6 | ask | ask | simplify (no technical details) | Market and business model |
| 7 | ask | ask | simplify (no technical jargon for AI/features) | Journeys; customer mode flags AI questions as [TECH-OPEN] |
| 8 | ask | ask | ask | UX is universal; show wireframes |
| 9 | ask | ask | ask | UI design; show mockups |
| 10 | skip / note as assumption | ask | TECH-OPEN (platforms deferred) | Developer may default to assumed stack; product owner decides; customer mode flags all as [TECH-OPEN] for design-interrogation |
| 11 | ask | ask | ask | Prototype walkthrough; all audiences validate |
| 12 | TECH-OPEN | ask | TECH-OPEN | Data/integration decisions; customer mode defers to Phase 12 technical interrogation |
| 13 | ask | ask | simplify (compliance explained simply) | Legal and risk; customer mode gets plain-language summary |
| 14 | TECH-OPEN | ask | TECH-OPEN | Constraints/operations/support; customer mode defers to design-interrogation |
| 15 | ask | ask | simplify | Launch & adoption; customer mode focuses on end-user adoption only |
| 16 | ask | ask | ask | Risks, assumptions, dependencies; simplified language for customer |
| 17 | ask | ask | ask (abbreviated) | Completeness check; customer mode: final review only; resume restricted to Phases 10, 12, 14, 16, 17 on return |

**Key:** ask = full questioning; simplify = same questions, plain language; TECH-OPEN = deferred to design-interrogation with [TECH-OPEN] flag; skip = phase not applicable.

## Interview Mechanics

The interview is structured around 18 phases (0–17), each resolving a major topic. The goal is to move fast without skipping depth.

- **One topic per round**, 1–4 related questions per round, answered by choosing wherever possible. This batching keeps the pace brisk and prevents decision fatigue.
- **Recommendations apply to decisions, not facts.** A choice ("PWA or store app?") carries my recommendation with reasoning, so you can accept it or reason differently. A fact the respondent owns ("who are your users?") is asked neutrally to avoid anchoring the answer.
- **"I don't know" is valid.** When the respondent cannot answer, it becomes `Assumption` (proceed with a flagged assumption, validation method named, owner assigned) or `Deferred` (decide later, with a named owner and target date) — it is never silently dropped.
- **Playback checkpoint** after every phase: a 3–5 line summary of what you've just decided. You confirm it or correct it before moving on. This prevents misunderstandings and creates a clear handoff point if the session is interrupted.
- **Show, don't only ask.** After Phase 8 (UX), wireframes are produced; after Phase 9 (UI), mockups are produced. You see them and react. Wireframes and mockups cover only the surfaces chosen in question 5.5 (provisional target surfaces; Phase 10 refines the list). Reactions are logged as decisions (Accept → Resolved; Change → Resolved plus a new PD; Reject → Conflict or Resolved; Question → Deferred). This is far better than describing what the product will look like.
- **Multiple stakeholders:** when more than one person is in the session, every decision records who said it. Conflicting answers are logged as `Conflict`, not averaged. The decision owner (identified in Phase 0) makes the final call.
- **Skip logic:** answers to product-type fork, platform choices, and whether AI features are present switch entire phases on or off. Skipped phases are recorded as not applicable, not left blank.
- **Confidentiality:** all discovery documents are written to `docs/product/` and `docs/input/`. The product brief and design briefs in `docs/product/` hold commercial secrets (pricing, roadmap, strategy); `docs/input/` may hold customer-provided data (screenshots, documents, Figma links saved for reference). Personas are fictional composites, never real people with real personal data. Research findings are referenced by date and source, not pasted wholesale. Before committing any discovery files to version control, confirm that the repository visibility is appropriate for sensitive content. Consider adding `docs/input/` to `.gitignore` if it will hold customer data that should not be stored in version control.
- **Bias guard:** questions are neutral and non-leading. We avoid solutioneering ("should this be a mobile app?") until the problem, audience, and value are settled. When the respondent proposes a solution instead of naming a need, we note it and ask "what problem would that solve?"

## Answer Ergonomics

The respondent should rarely have to compose an answer from scratch. Default to choosing; always allow typing.

Every question with a bounded answer set is asked as a choice via `AskUserQuestion` (single or multi-select). Free input is always available. Escape options (`Not sure yet`, `Decide later`, `Not applicable`) are first-class answers mapped to decision status in the log.

- **Multiple choice by default**, with `Other` always available. The respondent picks an option, or types their own answer anytime. This is stated once at the start so they know they are not constrained.
- **Free input always available** — no choice question forces an answer into an option. A typed answer is recorded verbatim and, if needed, normalised with the respondent's confirmation.
- **Option design:** 2–4 options per question, mutually exclusive unless multi-select (e.g., devices, languages, integrations). Each option has a plain-language label (1–5 words) plus a one-line consequence description so the respondent understands the impact. In Customer mode, descriptions avoid jargon. Recommended option marked `(Recommended)` — **for decisions only, never facts** (this avoids anchoring factual answers).
- **Visual options** when the choice is visual (layout, theme, density, card vs. list): options carry an ASCII preview or rendered sample so the respondent compares, not imagines.
- **Batching:** up to 4 related questions per round in one `AskUserQuestion` call. Follow-ups that depend on an earlier answer go in the next round.
- **Text questions (Mode: text):** Free-text questions without predefined options are asked once per round as a single numbered message. The respondent types an answer in plain chat language and is expected to label their response by question number if they answer multiple text questions in one turn (e.g., "1. Yes. 2. Dispatch managers. 3. Budget is tight."). Parse responses by number before moving to the next phase.
- **Larger option sets** (languages, countries, integrations, device features): split into a two-step choice (pick a group, then the items) or multi-select over the 4 likeliest items + `Other`.
- **Pre-filled answers:** when a value can be inferred (from codebase, existing documents, earlier answers, tech-stack.md), propose it as the first option labelled `(from {source})` so the respondent confirms with one click.
- **Fallback for clients without a choice tool** (Copilot, Reasonix Code, plain chat): render the same options as a lettered list and parse responses the same way. Free text is always accepted.
- **Pace controls:** a progress line each round (e.g., "Phase 3 of 18 — Users, about 2 rounds left"), *Skip this phase* and *Pause and save* available at playback checkpoints. The respondent can answer several questions with one typed message if they wish.

## Depth and Completeness

- **Two depth levels** per phase: *Core* questions are always asked and resolve the main decision. *Deep-dive* questions are asked when an answer is vague, risky, or drives a critical design or architecture decision later on. The respondent can also ask for deeper exploration, or say "enough on this."
- **Follow-up rule:** every answer is checked for four things: **number** (where a number is possible — e.g., "How many users?"), **named owner** (for decisions or tasks — e.g., "Who will write the copy?"), **example** (when the answer is abstract — e.g., "What is an example of a failure mode?"), **exception** (when the answer is broad — e.g., "Are there exceptions to this rule?"). Missing any of these triggers an immediate follow-up before the phase closes.
- **Completeness check (Phase 17):** a coverage checklist across all 18 phases (0–17). Any area still empty is either re-asked (if critical), or recorded as **not applicable / deferred / assumption** with its reason. The interview cannot be signed off with an unclassified gap.

## Phases 0–17 (Interview Outline)

The interview moves through 18 phases, each addressing one major topic. Phases are designed so that each resolves a topic completely before moving to the next — no backtracking needed. Skip logic (product-type fork, platform choices, AI flag) switches entire phases on or off.

See [`references/question-bank.md`](references/question-bank.md) for all questions, option sets, and response mappings. This table summarizes what each phase resolves and which decision IDs are logged:

| # | Phase | What | Outputs |
|---|-------|------|---------|
| 0 | Intake, respondent & governance | Mode, product-type fork, input docs, decision rights, product name, AI flag, stakeholder map (0.7), existing UI inventory (0.8) | PD (governance), discovery log starts |
| 1 | Problem & opportunity | Problem, workaround, cost, timing, evidence | PD (problem), problem statement |
| 2 | **Audience** | Segmentation, demographics, geography, digital skill, devices, context, accessibility, emotion, brand fit, safety, evidence | SEG, PD (audience), audience profile |
| 3 | Users & personas | Personas, jobs-to-be-done, context per persona | PD (personas), persona definitions |
| 4 | Value & success | Value per segment, business goals, KPIs, tracking plan, definition of done | GL, PD (value), tracking plan seed |
| 5 | Scope & release plan | MoSCoW, MVP, release phases, out-of-scope, kill criteria | PD (scope), MoSCoW list |
| 6 | Market & business model | Competitors, revenue, pricing, payments, tenancy, distribution | PD (market), competitive analysis |
| 7 | Journeys & functional needs | Top journeys, notifications, reporting, import/bulk, UGC, AI sub-block (conditional) | PD (journeys), journey maps |
| 8 | **UX** + wireframe show-back | IA, navigation, screens/states, onboarding, content & tone, forms, feedback, notifications, a11y, responsive | **Wireframes**; SCR, PD (UX reactions) |
| 9 | **UI & visual design** + mockup show-back | Brand/design system, accent colour → token generation, typography, themes, density, iconography, motion, deliverables | **Mockups**; PD (UI reactions), tokens |
| 10 | Platforms & deliverables | Matrix: web, mobile (iOS/Android), desktop (Windows, macOS), cross-surface, feature parity, DLV- register | DLV, PD (platforms), feature parity table |
| 11 | **Mocks & prototype** + validation | Assemble clickable prototype, walkthrough, validation round | **Prototype**; validation-log, walkthrough tasks |
| 12 | Data, content & integrations | Data ownership, migration, third parties, identity, reporting/analytics | PD (data), integration list |
| 13 | Compliance, legal & risk | GDPR, DPIA, industry rules, accessibility law, audit, licensing, T&Cs, security, brand/legal | PD (compliance), compliance register |
| 14 | Constraints, operations & support | Budget, deadline, team, stack, support model, release cadence, SLA, analytics, sustainability | PD (constraints), operations summary |
| 15 | Launch & adoption | Pilot/beta, launch date, migration, onboarding, marketing, success review, rollback plan | PD (launch), adoption plan |
| 16 | Risks, assumptions & audience validation | Top risks, assumptions to validate, audience assumptions from Phase 2 to validate, external dependencies, open questions | PD (risks), risk register |
| 17 | Completeness check, readback & sign-off | Coverage checklist, full playback, prototype sign-off, decision-owner confirmation, hand-off decision | PD log finalized, [TECH-OPEN] flagged |

## Phase 2 — Audience (Asked First, Shapes Everything Else)

The audience is asked early, in its own dedicated phase, because segment characteristics drive defaults for UX, UI, platform choices, and accessibility. Every primary, secondary, and tertiary segment is asked about in the same breadth: demographics, geography, digital skill, devices, context of use, accessibility needs, motivation, brand fit, and safeguarding. Segments are ranked (primary matters most).

For each segment, the respondent answers 11 categories of questions (see [`references/question-bank.md`](references/question-bank.md) Phase 2 for details). Evidence is logged alongside assumptions — what is known from research vs. what is guessed. Guesses are flagged for validation later (in Phase 16).

**Audience → Design Traceability Table** (captured in `audience-profile.md`, then copied to `ux-brief.md` and `ui-design-brief.md` so designers never have to cross-reference multiple documents):

| Audience finding | Constrains |
|---|---|
| Low digital skill / older users | Larger type, plain language, fewer choices/screen, guided onboarding, visible labels over icons |
| Mixed / poor connectivity, field use | Offline-first, sync-conflict policy, small payloads, large touch targets, high-contrast outdoor theme |
| Internal power users | Dense layouts, keyboard shortcuts, bulk actions, desktop-first |
| Many languages / RTL | Localisation architecture, layout mirroring, text-expansion room |
| High accessibility need / legal duty | WCAG level, assistive-tech test matrix, reduced-motion and high-contrast themes |
| Trust-sensitive task | Tone, confirmation patterns, security cues, undo and reassurance copy |
| Locked-down corporate devices | Installer type, admin rights, auto-update path, browser baseline |
| Minors or vulnerable users | Consent flows, content rules, data minimisation, moderation |

## Wireframes, Mockups & Clickable Prototype

Three fidelity levels are produced during the interview, each with its own show-back round. See [`references/prototype-guide.md`](references/prototype-guide.md) for full fidelity rules, show-back procedure, and accessibility verification. The reusable scaffold lives in [`assets/prototype-scaffold/`](assets/prototype-scaffold/) — a minimal dependency-free HTML/CSS/JS shell that runs from the file system with no server, no build step, no external services.

- **Wireframe** (Phase 8, end of UX): greyscale, real structure, placeholder content. Purpose: validate information architecture, navigation, flows, content hierarchy. Format: self-contained HTML under `docs/product/prototype/wireframes/`.
- **Mockup** (Phase 9, end of UI): high-fidelity static screens using generated tokens (accent colour → CSS variables), realistic persona-based content in the product's language. Purpose: validate look & feel, tone, density, brand fit. Format: HTML screens under `docs/product/prototype/mockups/`, per screen × surface (web, iOS, Android, Windows, macOS).
- **Clickable Prototype** (Phase 11): mockups wired into journeys with working navigation, forms with sample validation, state/theme/language toggles. Purpose: end-to-end walkthrough with real stakeholders; hand-off to design/build. Format: `docs/product/prototype/index.html`, fully navigable from the file system.

**Show-back round** after each level: present the visuals → ask task-based reactions (not "do you like it?" but "find X", "what would you do here?") → capture reactions as `PD-` decisions (accept / change / reject / question) → revise only what was rejected or flagged → re-show until decision owner approves.

**Delegation:** Designer + UI developer build wireframes and mockups; UI tester verifies prototype (navigation works, no dead screens, journeys complete, contrast passes, keyboard works, runs offline). Main conversation orchestrates the show-back round. Publish the prototype with the Artifact tool (private page) **only if the user explicitly asks** — never publish publicly without permission.

```
Wireframe ────→ Mockup ────→ Clickable Prototype
(Phase 8)       (Phase 9)    (Phase 11)
↓               ↓            ↓
PD decisions    PD decisions Show-back + walkthrough
from reactions  from reactions + validation-log
```

## Progressive Capture

Each resolved question is appended to `docs/product/discovery-decisions.md` immediately as a `PD-nnn` row. This ensures nothing is lost if the session is interrupted, and makes the final handoff a compilation rather than a cold generation from memory. The session is resumable — on start, the skill checks for an existing log and offers resume / amend / restart.

**Discovery IDs** (own prefixes, not validated by traceability regexes; strictly sequential): 
- `PD-nnn` — discovery decision (one per question resolved; status: Resolved / Assumption / Deferred / Conflict / N/A; flagged `[TECH-OPEN]` if a technical question is deferred to design-interrogation)
- `GL-nnn` — goal (from Phase 4; used in roadmap and roadmap sizing)
- `SEG-nnn` — audience segment (from Phase 2; each segment gets an ID)
- `SCR-nnn` — screen (from Phase 8/9; inventory in ux-brief and ui-design-brief)
- `DLV-nnn` — deliverable (from Phase 10; each shipping artifact has an owner, acceptance criterion, release phase)

**Flag semantics:** Decisions marked `[TECH-OPEN]` indicate unresolved technical questions (e.g., "Can we encrypt this offline?", "What's the sync conflict resolution strategy?") that Customer mode respondents cannot answer. These are listed explicitly in the closing summary and handed off to `design-interrogation` for technical resolution.

**Output documents** (all in `docs/product/`): See [`references/output-templates.md`](references/output-templates.md) for full templates including headers, status, respondents, and open items.
- `product-brief.md` — Executive summary: vision, problem, value per segment, business goals with measurement methods, MoSCoW scope, MVP, release plan, monetisation, launch & adoption, risks/assumptions, stakeholders & decision rights
- `audience-profile.md` — Ranked audience segments with per-segment answers to all Phase 2 questions, confidence levels (known vs. assumption), and audience → design traceability table
- `ux-brief.md` — Personas (built from segments), top journeys end-to-end, IA and navigation map, screen inventory (SCR-nnn with purpose, personas, states, components), content & tone of voice, forms & validation, feedback & undo, notifications & email, accessibility & localisation targets, responsive design rules
- `ui-design-brief.md` — Brand and visual identity, accent colour and token generation (light/dark/high-contrast), typography scale, themes and density, iconography and imagery, motion & animation, design deliverables and approval flow
- `platform-deliverables.md` — Surfaces matrix (web/iOS/Android/Windows/macOS with decisions per surface), feature parity table, deliverables register (DLV-nnn), distribution & update channels
- `discovery-decisions.md` — Live log (PD-nnn: decision, who said it, status Resolved/Assumption/Deferred/Conflict/N/A, rationale / validation method)
- `prototype/` folder — `wireframes/index.html` (low-fidelity), `mockups/` (high-fidelity per screen × surface), `index.html` (clickable prototype), `tokens.css` (generated from accent colour), `walkthrough.md` (scripted validation tasks), `validation-log.md` (results), `README.md` (build/handoff instructions)

## Output Compilation Procedure

As the interview progresses through phases, discovery documents are written incrementally (not generated after the fact):

1. **When written:** Each document is populated after its phase concludes:
   - After Phase 2 → `audience-profile.md` (segments, per-segment profiles, traceability table)
   - After Phase 3 → `ux-brief.md` (personas section)
   - After Phase 4 → `product-brief.md` (value & success, goals, tracking plan)
   - After Phase 5 → `product-brief.md` (scope & release plan)
   - After Phase 8 → Wireframes produced; `ux-brief.md` (IA, navigation, screen inventory, states)
   - After Phase 9 → Mockups produced; `ui-design-brief.md` (brand, tokens, typography, themes, density)
   - After Phase 10 → `platform-deliverables.md` (surfaces matrix, feature parity, DLV register)
   - After Phase 11 → Prototype assembled; `walkthrough.md` and `validation-log.md` recorded
   - After Phase 12 → `product-brief.md` (journeys, data, integrations)
   - After Phase 13 → `product-brief.md` (compliance, risks, sign-off section)
   - After Phase 17 → All documents finalized; status changed from "Draft" to "Confirmed"; decision owner signs off

2. **Prototype assembly (Phase 11):** Hand scaffolding + updated tokens + approved mockups + navigation wiring to `designer` and `ui-developer` subagents. They build index.html with all screens, state toggles, and navigation. Main session orchestrates the show-back round and validation.

3. **Validation (ui-tester):** After prototype is wired, run accessibility checklist: contrast, keyboard nav, screen reader, touch targets, reduced motion, offline operation.

4. **Status transitions:** Mark "Draft" at creation. Change to "Confirmed" only when decision owner has reviewed and signed off (typically Phase 17 completion). Never revert to Draft once Confirmed without explicit decision owner approval.

5. **Archive on start-over:** If the session is restarted (not resumed, but completely started over), archive prior discovery-decisions.md and all related briefs to `docs/product/archive/{yyyy-mm-dd}/` (with today's date). This preserves prior work for reference without cluttering the active discovery tree.

## Sign-Off and Hand-Off

At the end of Phase 17 (Completeness Check), when the decision owner confirms that the product brief is accurate and complete:

> **Ready to build.** Run [`design-interrogation`](../design-interrogation/SKILL.md) — it will read `docs/product/*` as pre-resolved input. Every `PD-nnn` decision is marked with its source in the session-decisions log, so interrogation focuses only on the remaining technical dimensions (architecture, identity & access, data management, delivery, operations, testing, and AI/ML if present).

The skill does not generate an architecture document, select a technology stack, or interrogate technical dimensions. That is the job of [`design-interrogation`](../design-interrogation/SKILL.md). Discovery answers the **what** and **why**; interrogation answers the **how** and **with what**.

## Closing Summary Template

At the end of the interview (Phase 17 sign-off), the skill presents this summary:

```
## Discovery Complete — {Product Name}

**Respondents:** {Names and roles}
**Interview dates:** {Start date} – {End date}
**Interview length:** {approx. hours}
**Total decisions logged:** {N}
**Status breakdown:** Resolved {N} · Assumptions {N} · Deferred {N} · Conflict {N} · N/A {N}

## Deliverables in `docs/product/`
✅ product-brief.md — vision, problem, value per segment, business goals, MoSCoW scope, release plan, launch & adoption, risks/assumptions
✅ audience-profile.md — 3 ranked segments, per-segment profile, design traceability
✅ ux-brief.md — personas, top journeys end-to-end, IA/navigation, screen inventory (SCR-nnn), content & tone, forms, accessibility & localisation
✅ ui-design-brief.md — brand & visual identity, tokens (light/dark/high-contrast), typography, density, themes, motion & animation
✅ platform-deliverables.md — surfaces matrix, feature parity, deliverables register (DLV-nnn), distribution & update channels
✅ prototype/ — wireframes, mockups, clickable prototype (index.html), walkthrough.md, validation-log.md, README.md
✅ discovery-decisions.md — PD-nnn log with all 18 phases (0–17), status (Resolved/Assumption/Deferred/Conflict/N/A), rationale

**Open items (if any):**
- {List any decisions deferred to v1.1 or assumptions needing validation}

**Confidentiality note:** This brief contains commercial details (pricing, roadmap, strategy). Check repository visibility before committing.

## Next Step
Run [`design-interrogation`](../design-interrogation/SKILL.md) to complete the Product Specification and architecture document.
```

### Customer Mode Phase 17 (Abbreviated)

When the respondent is a Customer or Business Stakeholder, Phase 17 is abbreviated to a **draft sign-off only**:
- Review the summary of decisions (no re-asking of resolved items)
- Confirm product brief, UX/UI briefs, and prototype are ready
- Decision owner approves with sign-off date
- Status: "Draft — awaiting technical pass"

**Resume restrictions:** If a session is interrupted and resumed, Customer mode can only jump to Phases 10 (Platforms), 12 (Data/Integrations), 14 (Constraints), 16 (Risks), or 17 (Completeness) to make late corrections. Full re-interview is not possible mid-stream; use **Amend** mode to revisit specific decisions.

## Example Exchange (Customer Mode)

**Respondent mode:** Customer / Business Stakeholder

**Round context:** Phase 2, Audience Type & Segmentation

**Skill:**

> **Who uses this product?** Which groups are customers, and which matters most?
> 
> - *B2C (individual consumers)* — People buy for themselves
> - *B2B (business customers)* — Companies buy for their teams
> - *B2E (internal staff)* — We build this for our employees
> - *Mixed* — Two or more of the above
> 
> Pick an option, or type your own answer anytime.

**Respondent:** We're targeting small logistics yards—so businesses. B2B.

**Skill:**

> Got it, B2B. How many yards now, and how many in 3 years?

**Respondent:** 50 yards right now. We're hoping to scale to 500 by 2029.

**Skill:**

> *Logged to discovery-decisions.md: PD-021 — Audience: B2B, 50 yards (now), 500 (3 years).*
>
> Next question: who *buys* this (the owner?), who *uses* it (the dispatcher?), and who *decides* (maybe both)?

## Related Skills

| Skill | When |
|-------|------|
| [`design-interrogation`](../design-interrogation/SKILL.md) | **Downstream** — consumes this skill's output; interrogates technical dimensions |
| [`ubiquitous-language`](../ubiquitous-language/SKILL.md) | **Active during session** — capture domain terms as they emerge |
| [`usecase-specification`](../usecase-specification/SKILL.md) | **Active during session** — draft use cases as flows resolve |
| [`user-story`](../user-story/SKILL.md) | **Active during session** — draft stories as acceptance criteria emerge |
| [`css-theme-generator`](../css-theme-generator/SKILL.md) | **Outputs** — turn accent colour into tokens for mockups + prototype |
| [`xaml-theme-generator`](../xaml-theme-generator/SKILL.md) | **Outputs** — platform tokens (framework recorded as [TECH-OPEN] for design-interrogation) |
| [`playwright-tester`](../playwright-tester/SKILL.md) | **Outputs** — E2E test against prototype baseline |
| `designer` | **Outputs** — refine component usage and design decisions |
| `ui-developer` | **Outputs** — build surfaces from approved mockups |
| `ui-tester` | **Outputs** — verify prototype navigation, states, contrast, keyboard |
| `council` | **Policy** — not needed; change is additive, backward-compatible |
