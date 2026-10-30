# Product Discovery Skill + Design Interrogation Completion

Status: DONE (2026-10-30) — implemented; see .ai/completed/product-discovery-skill.md
Started: 2026-10-30
Requested by: user — "As a developer, product owner or even customer I want to be interviewed when I create a new product. Cover UI, UX, design and deliverables (web, mobile, desktop). The interview should be as complete as possible; at the end we have a clear view of what we are going to build combined with the technical requirements. If design-interrogation is not complete enough, complete it." Revision 2 added the audience phase; revision 3 adds mocks and clickable demos as outputs and closes the gaps found in a self-review (listed in *Gap register*).

## Goal

Close the gap upstream of `design-interrogation`. Today the template can interview about *architecture*; nothing interviews about the *product* (problem, audience, value, UX, UI, platforms, deliverables), nothing *shows* the respondent what they are asking for, and `design-interrogation` has no dimension for client surfaces, identity, data/privacy, delivery, operations or testing. After this change:

1. A new **`product-discovery`** skill runs a plain-language, role-aware interview (developer / product owner / customer), shows **wireframes, mockups and a clickable prototype** as it goes, and produces a product brief set.
2. **`design-interrogation`** consumes that set as pre-resolved input, completes the missing technical dimensions, and finishes by producing one consolidated **Product Specification** that joins *what we build* (including the prototype) with *the technical requirements*.

## Decisions (answered 2026-10-30)

1. **Document language:** English; the interview runs in the respondent's language. Mock/prototype *content* uses the product's own language(s).
2. **Output folder:** `docs/product/`.
3. **Customer mode:** a customer may run the interview alone; technical gaps are flagged `[TECH-OPEN]` and settled in `design-interrogation`.
4. **Desktop scope:** Windows and macOS (Linux is not offered as a deliverable option).
5. **Audience:** a dedicated phase, asked before users, UX and UI, with an audience → design traceability table.
6. **Mocks and clickable demos:** first-class outputs (wireframes → mockups → clickable prototype), built during the interview, not after it.

## Council check

No council. The change is additive and backward-compatible (new skill; new dimensions appended, existing numbering kept); it alters no architecture decision, public contract, security posture or data. Per `AGENTS.md` → *When to Convene a Council* no trigger fires. (The extended `design-interrogation` additionally learns to *flag* council triggers it meets — gap 17.)

## Existing types / assets reused (no duplicates created)

| Asset | Reuse |
|---|---|
| `.ai/skills/design-interrogation/SKILL.md` | Extended in place — not forked |
| `ubiquitous-language`, `usecase-specification`, `user-story` | Loaded by discovery too; discovery drafts feed their Mode 0/1 |
| `.ai/reference/quality-model.md` | Dimension 7 vocabulary unchanged; discovery pre-answers *Interaction capability* |
| `css-theme-generator`, `blazor-theme-generator`, `xaml-theme-generator`, `maui-apple-design` | Used to turn the accent colour into tokens that the mockups and prototype consume — not re-implemented |
| `blazor-fluentui`, `ui-blazor`, `ui-maui`, `ui-winui`, `ui-wpf` | Read to learn which components exist, so mocks only use buildable components |
| `designer`, `ui-developer`, `ui-tester` agents; `playwright-tester` skill | Build and verify the mocks and prototype |
| `.ai/project/tech-stack.md`, `forbidden-tech.md`, `standards.md` | Read to pre-fill constraints and compliance |
| `docs/session-decisions.md` log pattern | Mirrored by `docs/product/discovery-decisions.md` |
| `Artifact` tool | Optional private publishing of the prototype — only on the user's request |

New types: one skill, its reference files, one output template set, one prototype scaffold. A solution-wide search for `product-discovery` / `product-brief` / `prototype` found nothing to reuse (re-verify at step 1).

## Part A — `product-discovery` skill

Location: `.ai/skills/product-discovery/`
- `SKILL.md` — protocol, respondent modes, phases, capture rules, hand-off (target ≤ 400 lines)
- `references/question-bank.md` — every question per phase at *core* and *deep-dive* level, plain-language rewrites, and the curated **option set** for each question (labels, one-line descriptions, single/multi-select, previews, mapping to decision status)
- `references/output-templates.md` — templates for the documents
- `references/prototype-guide.md` — how to build wireframes, mockups and the clickable prototype (fidelity levels, scaffold, state toggles, walkthrough script, validation round)
- `assets/prototype-scaffold/` — a minimal dependency-free HTML/CSS/JS prototype shell (device frames, screen router, state/theme/language toggles, token file hook)

### Interview mechanics

- **Respondent mode** asked first: *Developer*, *Product owner*, *Customer / business stakeholder*, or *Mixed*. Mode changes vocabulary and depth, never coverage: Customer mode never mentions CQRS or aggregates and routes technical gaps to `design-interrogation` as `[TECH-OPEN]`; Developer mode may be terse and codebase-aware.
- **One topic per round**, 1–4 questions per round, answered by choosing wherever possible (see *Answer ergonomics*).
- **Recommendations apply to decisions, not facts.** A choice ("PWA or store app?") carries *My recommendation* with reasoning, as in `design-interrogation`. A fact the respondent owns ("who are your users?") is asked **without** a recommendation, to avoid anchoring the answer; the skill may then offer an interpretation to confirm.
- **"I don't know" is a valid answer.** It becomes `Assumption` (proceed, flagged, validation method named) or `Deferred` (decide later, owner named) — never silently dropped.
- **Playback checkpoint** after every phase: a 3–5 line summary the respondent confirms or corrects.
- **Show, don't only ask.** After the UX and UI phases the skill produces wireframes and mockups and asks for reactions; reactions are logged as decisions (see *Mocks, mockups and clickable prototype*).
- **Multiple stakeholders:** every decision records *who said it*; conflicting answers are logged as `Conflict`, not averaged. Phase 0 identifies who has decision rights.
- **Skip logic:** platform, product-type and AI answers switch whole phases or sub-blocks on or off. Skipped = recorded *not applicable*.
- **Progressive capture:** each resolved question is appended to `docs/product/discovery-decisions.md` immediately (`PD-001`, …); the session is resumable — on start the skill checks for an existing log and offers *resume / amend / start over*.
- **Responds in the respondent's language**; trigger phrases in the skill description cover English and Dutch.
- **Confidentiality.** Outputs may hold commercial secrets. Personas are fictional composites — no real people's personal data; real research data is referenced, not pasted. The skill tells the user where files are written and reminds them to check repository visibility before committing.
- **Bias guard.** Questions are neutral and non-leading; the skill avoids solutioneering ("should it be an app?") before the problem and audience are settled, and records when the respondent proposed a solution instead of a need.

### Answer ergonomics — easy to respond, free input always possible

The respondent should rarely have to compose an answer from scratch. Default to choosing; always allow typing.

- **Multiple choice by default.** Every question that has a bounded set of sensible answers is asked as a choice through `AskUserQuestion` (single-select, or multi-select where answers are not mutually exclusive, e.g. devices, languages, integrations). Open questions are asked as text only when no useful option set exists (problem statement, a story in their own words).
- **Free input is always available.** Every choice question offers *Other* (the tool adds it automatically) and the skill says so once at the start: *"Pick an option, or type your own answer at any time."* A typed answer is never forced into an option; it is recorded verbatim and, if needed, normalised with the respondent's confirmation.
- **Escape options are first-class.** Where it makes sense, an option set includes *Not sure yet* (→ Assumption), *Decide later* (→ Deferred, owner asked next) and *Not applicable* (→ N/A). The respondent never has to invent an answer to move on.
- **Option design rules.** 2–4 options per question (tool limit), mutually exclusive unless multi-select, plain-language label of 1–5 words plus a one-line consequence description, no jargon in Customer mode, the recommended option first and marked *(Recommended)* — **only for decisions**, never for facts (see recommendations rule). Larger option sets (languages, countries, integrations, device features) are split into a **two-step choice** (pick a group, then the items) or asked as multi-select over the 4 most likely items plus *Other*.
- **Batching.** Up to 4 related questions per round in a single `AskUserQuestion` call, so a phase takes 2–4 rounds, not 20. Follow-ups that depend on an earlier answer go in the next round.
- **Visual options.** When the choice is visual (layout, navigation pattern, density, card vs list, theme mood), options carry a `preview` — an ASCII layout or a tiny rendered sample — so the respondent compares rather than imagines. Mockup and prototype reactions use fixed choice sets: *Accept / Change (say what) / Reject / Question*, and task results use *Succeeded / Struggled / Failed*.
- **Reaction shortcuts.** After each playback checkpoint: *Correct / Mostly, with changes / No, redo this* — the "changes" path opens a free-text follow-up.
- **Pre-filled answers.** When a value can be inferred (from documents, codebase, earlier answers, tech-stack.md), the skill proposes it as the first option labelled *(from {source})* so the respondent confirms with one click.
- **Option sets are curated, not improvised.** `references/question-bank.md` holds, per question, the option set, descriptions, multi-select flag, and the answer's mapping to a decision status and downstream constraint; the skill reuses it so answers are consistent across sessions.
- **Fallback when the client has no choice tool** (Copilot, Reasonix, plain chat): the same options are rendered as a lettered list in text — *"Reply A, C, or write your own"* — and parsed the same way. Free text is always accepted.
- **Pace and fatigue controls.** A progress line each round (*Phase 3 of 18 — Users, about 2 rounds left*), *Skip this phase* and *Pause and save* available at every playback checkpoint, and the respondent may answer several questions with one typed message.
- **Language and tone.** Questions, options and descriptions are phrased in the respondent's language and role vocabulary (Customer mode: outcomes and examples, not technical terms).

### Depth and completeness

- **Two depth levels per phase.** *Core* questions are always asked; *deep-dive* questions are asked whenever an answer is vague, risky, or drives a design or architecture decision. The respondent can say "go deeper" or "enough on this" at any time.
- **Follow-up rule.** Every answer is checked for: a number where a number is possible, a named owner, an example, an exception. A missing one triggers a follow-up before the phase closes.
- **Completeness check (final phase).** A coverage checklist is run over all phases; any area still empty is re-asked, or recorded as not applicable / deferred / assumption with its reason. The interview cannot be signed off with an unclassified area.

### Product type fork (Phase 0)

The first questions decide the interview path:

| Situation | Effect |
|---|---|
| **New product** (greenfield) | Full path |
| **New capability in an existing product** | Codebase, analytics and existing docs are read first; audience/brand/design-system phases are *confirm and amend*; existing UI is captured as screenshots/inventory and the prototype extends it |
| **Replacement / migration** | Adds current-system pain points, must-keep behaviour, data migration, parallel-run and switch-over questions |
| **Internal tool vs customer-facing vs platform/API product** | Changes defaults: internal → density and keyboard; customer-facing → brand and onboarding; platform → developer experience, docs, SDK |
| **Contains AI/ML features** | Enables the AI sub-block in Phase 7 |

### Phases

| # | Phase | What is resolved |
|---|---|---|
| 0 | Intake, respondent & governance | Mode, product-type fork, existing documents/screenshots/Figma links (saved to `docs/input/`), who else must be heard, **decision rights** (who signs off scope, design, budget), product name & working title, domain/trademark awareness |
| 1 | Problem & opportunity | Problem statement, who has it, how it is solved today, cost of not solving, why now, evidence |
| 2 | **Audience** | Who the product is for — *Phase 2 — Audience* below. Resolved **before** users, UX and UI because it drives all three |
| 3 | Users & personas | Primary / secondary / admin / external users built *from* the audience segments, jobs-to-be-done, context of use (desk, field, offline, in motion), support and training needs |
| 4 | Value & success | Value proposition per segment, business goals, success metrics with numbers (KPIs/OKRs), **how each metric will be measured** (the seed of the tracking plan), definition of done for v1 |
| 5 | Scope & release plan | Capabilities as MoSCoW, MVP boundary, release phases, explicit out-of-scope, kill criteria |
| 6 | Market & business model | Alternatives and competitors (screenshots welcome), differentiation, revenue and pricing model, **monetisation mechanics** (subscription, in-app purchase, invoicing, trials, refunds), payment/tax/VAT implications, app-store commercial rules, tenancy (single vs multi-tenant, white-label) |
| 7 | Journeys & functional needs | Top journeys end to end, triggers, outcomes, edge cases, notifications, reporting/export, search, admin tasks, **import/bulk operations**, **user-generated content & moderation**. **AI sub-block (conditional):** what the AI does, human oversight, acceptable error rate, data used, transparency/explanation to users, fallback when it fails, cost per call, EU AI Act risk class |
| 8 | **UX** + *wireframe show-back* | Information architecture, navigation model, key screens/states (empty, loading, error, offline, success, no-permission), onboarding, content & tone of voice, forms & validation behaviour, feedback & undo, notifications & e-mail design, accessibility target (WCAG 2.2 AA default; EN 301 549 / European Accessibility Act where applicable), localisation (languages, RTL, formats, time zones, currencies), responsive behaviour, content ownership (who writes copy, help centre, legal text), UX research evidence available. **Ends by producing low-fidelity wireframes of the top journeys for reaction.** |
| 9 | **UI & visual design** + *mockup show-back* | Existing brand/design system/Figma, logo & assets, accent colour (hex/HSL) → theme skills → tokens, typography, light/dark/high-contrast, density, iconography, imagery/illustration style, motion & haptics, component library (Fluent UI default per template), design deliverables wanted, who approves design. **Ends by producing high-fidelity mockups** of the key screens per surface using the generated tokens, for reaction |
| 10 | **Platforms & deliverables** | Matrix below |
| 11 | **Mocks & clickable prototype** | Assemble the clickable prototype from the approved wireframes/mockups, run the walkthrough and validation round — *Mocks, mockups and clickable prototype* below |
| 12 | Data, content & integrations (business view) | Data the product owns vs imports, migration of existing data, third parties (payments, identity, maps, e-mail/SMS/push, ERP/CRM), identity (SSO, social, B2B directory), reporting/analytics needs, email/notification providers |
| 13 | Compliance, legal & risk | GDPR / data residency, DPIA need, industry rules, accessibility law, audit/retention, minors' data, licensing and open-source obligations, terms/privacy policy/cookie consent ownership, store policy compliance, security expectations, brand/legal risk |
| 14 | Constraints, operations & support | Budget, deadline, team size/skills, existing stack/hosting, support model and tiers, release cadence, SLA expectations, analytics/telemetry & feedback loops, sustainability or performance budgets, maintenance ownership after launch |
| 15 | Launch & adoption | Pilot/beta plan, launch date drivers, migration of first customers, onboarding and training, marketing site, communications, success review date, rollback/communication plan |
| 16 | Risks, assumptions, dependencies | Top risks with owner, assumptions to validate (with method and date), external dependencies, open questions |
| 17 | Completeness check, readback & sign-off | Coverage checklist across all phases, full playback of the brief, prototype sign-off, explicit "this is what we will build" confirmation by the decision owner, hand-off decision |

### Phase 2 — Audience

The audience is asked early, in its own phase, because it sets the defaults for UX, UI and platform choices. It is asked for **every segment** (primary, secondary, tertiary), and the segments are ranked.

| Area | Questions |
|---|---|
| **Type & size** | Consumer (B2C), business customers (B2B), internal staff, partners/resellers, public/citizens, or a mix? How many people per segment now and in 3 years? Who *buys* vs who *uses* vs who *decides*? |
| **Demographics** | Age range, life stage, profession/role, education, income band where it affects pricing or channels |
| **Geography & language** | Countries/regions, languages, reading level (plain-language target), cultural conventions (colour meaning, imagery, date/number/address/name formats, RTL), legal region |
| **Digital skill & habits** | Tech literacy, familiarity with comparable products, expectations set by apps they already use, patience for onboarding, preferred channels |
| **Devices & connectivity** | Devices owned and actually used (phone, tablet, laptop, shared/kiosk, older hardware), OS and browser mix, screen sizes, bandwidth, offline periods, managed/locked-down corporate machines |
| **Context of use** | Where and when (office, field, vehicle, home, while walking, noisy/bright environment), single-handed use, interruptions, session length and frequency, shared devices |
| **Accessibility & inclusion** | Share of users with visual, hearing, motor, cognitive needs; screen-reader, zoom, voice, switch, reduced-motion use; colour-blindness; age-related needs; legal obligations (EAA, WCAG level) |
| **Motivation & emotion** | Why they come, what frustrates them today, stress level of the task (e.g. payments, health), trust sensitivity, desired feeling (calm, playful, authoritative, premium) |
| **Brand & tone fit** | Formal vs informal address, humour allowed, brand personality, voice examples they like and dislike, competitors' look they want to resemble or avoid |
| **Access & safeguarding** | Minors, vulnerable people, consent and guardianship, safety-critical use |
| **Evidence** | Existing research, analytics, support tickets, interviews, surveys, personas; what is known vs guessed (guesses are logged as Assumptions to validate) |

**Audience → design traceability.** Each audience answer is mapped to the decision it constrains, recorded in `audience-profile.md` and re-checked in the final phase:

| Audience finding | Constrains |
|---|---|
| Low digital skill / older users | Larger type and targets, plain language, fewer choices per screen, guided onboarding, visible labels over icon-only |
| Mixed or poor connectivity, field use | Offline-first, sync-conflict policy, small payloads, large touch targets, high-contrast outdoor theme |
| Internal power users | Dense layouts, keyboard shortcuts, bulk actions, desktop-first |
| Many languages / RTL | Localisation architecture, layout mirroring, text-expansion room |
| High accessibility need or legal duty | WCAG level, assistive-tech test matrix, reduced-motion and high-contrast themes |
| Trust-sensitive task | Tone, confirmation patterns, security cues, undo and reassurance copy |
| Locked-down corporate devices | Installer type, admin rights, auto-update path, browser baseline |
| Minors or vulnerable users | Consent flows, content rules, data minimisation, moderation |

### Phase 10 — Platforms & deliverables matrix

Resolved per surface; each answer carries an in/out/later status and a priority.

| Surface | Questions |
|---|---|
| **Web** | Public site vs authenticated app vs both; Blazor Server / WASM / Auto vs static; PWA/installable; supported browsers and minimum versions; responsive breakpoints; SEO/SSR needs; embed/widget; performance budget |
| **Mobile** | iOS / Android / both; phone / tablet; native-feel vs shared UI; MAUI vs Blazor Hybrid vs responsive web only; offline-first and sync; device features (camera, GPS, biometrics, push, NFC, Bluetooth, files); minimum OS versions; store distribution (public, private/enterprise, MDM); release and review ownership |
| **Desktop (Windows, macOS)** | WinUI / WPF / MAUI Mac Catalyst; installer & packaging (MSIX, MSI, PKG/DMG, store, portable); auto-update channel; offline & local storage; OS integration (tray/menu bar, file associations, shell, printing); admin-rights and managed-device constraints; code signing/notarisation ownership |
| **Cross-surface** | What must be identical vs platform-idiomatic; shared-code strategy; feature parity table; account/session continuity; one backend vs per-surface BFF |
| **Other deliverables** | Public API / SDK (Kiota client), admin portal, back-office, documentation site, onboarding material, marketing site, training, support runbooks, demo/sandbox environment, **accessibility statement**, **design system / token package**, **prototype hand-over** |

Output: a **deliverables register** (`DLV-nnn`) — each deliverable with owner, acceptance criterion, platform, release phase.

### Mocks, mockups and clickable prototype

The respondent reacts far better to something visible than to a description, so visuals are produced *during* the interview at three fidelity levels, each with its own show-back:

| Level | When | What it is | Purpose | Format |
|---|---|---|---|---|
| **Wireframe** | End of Phase 8 | Greyscale, real structure, placeholder content, one per top-journey screen | Validate information architecture, navigation, flows, content hierarchy before any visual design | Self-contained HTML (+ exported PNG on request) under `docs/product/prototype/wireframes/` |
| **Mockup** | End of Phase 9 | High-fidelity static screens in the real tokens (accent colour, type, light/dark), realistic persona-based content in the product's language, per surface (web, phone, tablet, Windows, macOS) with platform-idiomatic chrome | Validate look & feel, tone, density, brand fit for the audience | HTML screens under `.../mockups/`, one per screen × surface; state variants (empty/loading/error/offline) for key screens |
| **Clickable prototype** | Phase 11 | The mockups wired into the journeys: working navigation, forms with sample validation, state/theme/language/device toggles, scripted happy path plus main error paths | Walkthrough and validation with real stakeholders; hand-over to design/build | `docs/product/prototype/index.html` + assets, runs from the file system with no build step or server |

**Rules for all three**

- **Built only from components that exist.** Mocks may only use components available in the chosen UI library (Fluent UI for Blazor, MAUI controls, WinUI/WPF controls). Anything custom is marked `custom` in the screen inventory so the cost is visible. This keeps the mocks buildable.
- **Tokens from the accent colour** via `css-theme-generator` (and `blazor-theme-generator` / `xaml-theme-generator` for the matching platform tokens). One token file feeds mocks, prototype and later the product.
- **Audience-driven.** Type size, density, target size, contrast, tone and device frames follow `audience-profile.md`; every mock lists the audience findings it applies.
- **Realistic content.** Persona-based sample data, in the product's real language(s); no lorem ipsum, no real people's data.
- **Accessible by construction.** Contrast of the token pairs checked against the agreed WCAG level before the show-back; focus order, labels and target sizes follow the agreed target; reduced-motion respected.
- **Surface-aware.** The prototype switches between device frames and platform idioms (web responsive widths, iOS/Android phone and tablet, Windows, macOS). Where a feature differs per platform, the parity table says so.
- **Toggles** for: theme (light/dark/high-contrast), language/RTL (when multilingual), screen state (empty/loading/error/offline/success/no-permission), and persona/role (e.g. admin vs user).
- **Screen inventory** — every screen gets `SCR-nnn`, with purpose, persona, journey, states, component list, `custom` flags, and the `PD-` decisions it embodies.
- **Marked as a prototype.** Visibly labelled "Prototype — not the product"; no real credentials, no calls to real services, no real personal data.
- **Local first.** Files live in the repository under `docs/product/prototype/`. Publishing as a private Artifact page for stakeholders is offered, never done without the user's say-so (it is outward-facing).

**Show-back round (all three levels).** Present → task-based reactions ("find X", "what would you do here?") → capture reactions as `PD-` decisions (*accepted / change / reject / question*) → revise → re-show only what changed. The loop ends when the decision owner accepts the level.

**Walkthrough and validation (Phase 11).** A scripted walkthrough with 5–8 tasks derived from the top journeys, each with a success criterion; run with the respondent and, where possible, with representatives of each primary audience segment; results recorded in `docs/product/prototype/validation-log.md` (task, who, success/fail, observation, resulting `PD-` change). Unresolved findings enter the risks list.

**Verification.** Built by `designer` + `ui-developer`; checked by `ui-tester` / `playwright-tester` for: every link/navigation works, no dead screens, all journeys completable, state toggles render, contrast and keyboard checks pass, runs offline from the file system.

### Output documents and files (`docs/product/`)

Six documents plus the prototype. `ux-brief.md` and `ui-design-brief.md` each open with a *Design implications of the audience* section copied from `audience-profile.md`, so designers never cross-reference.

| File | Content | Primary consumer |
|---|---|---|
| `product-brief.md` | Vision, problem, value, goals & metrics (with measurement), MoSCoW scope, release plan, monetisation, launch & adoption plan, risks/assumptions, stakeholders & decision rights | `design-interrogation` Phase -1 |
| `audience-profile.md` | Ranked audience segments, per-segment answers to every Phase 2 area, evidence vs assumption, audience → design traceability table | `ux-brief`, `ui-design-brief`, `design-interrogation` (Dimensions 7 and 9) |
| `ux-brief.md` | Personas, journeys, IA/navigation map, **screen inventory (`SCR-`)**, accessibility & localisation targets, content principles, notification/e-mail inventory | `designer`, `ui-developer`, `user-story` |
| `ui-design-brief.md` | Brand inputs, accent colour and generated tokens, typography, theme modes, component library and `custom` list, design-deliverable list and approvals | theme-generator skills, `designer` |
| `platform-deliverables.md` | Surface matrix, feature-parity table, deliverables register (`DLV-`), distribution & update channels | `architect`, `solution-generator`, `ui-*` skills |
| `discovery-decisions.md` | Live log (`PD-nnn`: decision, who, status Resolved/Assumption/Deferred/Conflict/N-A, rationale) | all of the above |
| `prototype/` | `wireframes/`, `mockups/`, `index.html` clickable prototype, `tokens.css`, `walkthrough.md` (task script), `validation-log.md` | stakeholders, `designer`, `ui-developer`, `ui-tester` |

Every document starts with a **Status** (Draft / Confirmed), the respondents, and a list of open items. Persona names are reused verbatim by `user-story` ("As {persona}").

**Discovery IDs** (own prefixes, not validated by `validate-traceability.py`, whose scan regexes only match `US|UC|AC|AF-{BC}-{NNN}`): `PD-` decision, `GL-` goal, `SEG-` audience segment, `SCR-` screen, `DLV-` deliverable.

### Hand-off

On sign-off, the skill states the next step explicitly: *"Run `design-interrogation` — it will read `docs/product/` as pre-resolved input."* It does not generate architecture itself.

## Part B — complete `design-interrogation`

### Gap analysis (what is missing today)

| # | Gap in the current skill | Fix |
|---|---|---|
| 1 | Phase -1 treats every input as a generic document; no knowledge of a product brief | Recognise `docs/product/*`; import each `PD-nnn` as **Pre-Resolved** with its ID in a new *Source* column; do not re-ask |
| 2 | Phase 0 has no question about target platforms or surfaces | Add **A5 — Surfaces & Deliverables** (pre-filled from `platform-deliverables.md` when present) |
| 3 | No dimension for the client side: render mode, shared-UI strategy, state management, navigation, design system, offline/sync, per-platform packaging | Add **Dimension 9 — Client Surfaces & UX Architecture** |
| 4 | Authn/authz, tenancy and roles appear only as a single Security row in Dimension 7 | Add **Dimension 10 — Identity, Access & Tenancy** |
| 5 | Persistence, retention, privacy (GDPR), backup/restore, data migration are not interrogated | Add **Dimension 11 — Data Management & Privacy** |
| 6 | Environments, CI/CD, release channels (stores, installers, auto-update), hosting and cost are not interrogated beyond "rollout" | Add **Dimension 12 — Delivery, Environments & Hosting** |
| 7 | Logging, metrics, tracing, alerting, analytics, support tooling and runbooks are not interrogated | Add **Dimension 13 — Observability & Operations** (includes the **tracking plan** that implements the discovery metrics) |
| 8 | Test strategy is not an interrogated decision | Add **Dimension 14 — Testing Strategy** |
| 9 | Dimension 7 *Interaction capability* is one generic question | Keep; mark **pre-resolved from `ux-brief.md` / `audience-profile.md`** when discovery ran, else ask it |
| 10 | No consolidated artefact — nothing states *what we build + technical requirements* in one place | Add **Deliverable 4 — Product Specification** |
| 11 | Hand-off pipeline stops at `solution-generator` → `vertical-slices` → `gap-review`; UI/design/platform skills are not wired in | Extend Step 5 with theme-generator, `designer`, `ui-*`, `maui-apple-design`, `playwright-tester` hand-offs and the **prototype as a UI acceptance reference** |
| 12 | Step 1 loads "any instruction files" without naming them | Name `tech-stack.md`, `forbidden-tech.md`, `architecture.md`, `quality-model.md`, `standards.md` so constraints (A4) are pre-filled by reading, not asking |
| 13 | Closing summary lists three deliverables | Add the Product Specification row and a *Traceability coverage* line |
| 14 | Related Skills table does not mention the upstream skill | Add `product-discovery` |
| 15 | No AI/ML dimension although AI features are now common | Add conditional **Dimension 15 — AI/ML Features** (asked only when discovery or the user flags AI): model/provider choice and swap-ability, prompt/data handling and privacy, evaluation and quality gates, human-in-the-loop, cost and rate limits, safety/abuse controls, transparency, EU AI Act classification |
| 16 | No feasibility check: nothing compares the wished-for scope with budget, deadline and team | Product Specification gains a **Roadmap & rough sizing** section (T-shirt size per capability, critical path, scope-vs-budget/deadline verdict, MVP cut proposal when it does not fit) |
| 17 | High-stakes decisions surfaced by the interview are not routed to the council | When a decision meets a council trigger (`AGENTS.md`), flag it **"Council recommended"** in `session-decisions.md` and the closing summary instead of deciding it silently |
| 18 | No resume path if the session is interrupted | On start, detect `docs/session-decisions.md`; offer resume / amend / restart |
| 19 | Compliance requirements are scattered | Product Specification gains a **Compliance register** (requirement, source, owner, how verified), cross-checked against `standards.md` |
| 20 | Prototype and design never meet the build | Dimension 9 includes "how does the build stay faithful to the prototype": token source of truth, component mapping, visual-regression baseline from the mockups, design review gate |
| 21 | Dimension numbering would be misleading once 9–15 are appended | Keep 1–8 numbers (other files cite "Dimension 7/8"); add an *Interrogation order* table giving the dependency order (identity and data before client surfaces; delivery, operations and testing last) |

### New dimensions — key questions

| # | Dimension | Resolves |
|---|---|---|
| 9 | Client Surfaces & UX Architecture | Per surface from A5: render/host model (Blazor Server/WASM/Auto/Hybrid/MAUI/WinUI/WPF), shared UI library vs per-platform, navigation & state management, design-system/tokens implementation, theming (light/dark/high-contrast), responsive and adaptive rules, offline & sync conflict policy, device-API access, localisation mechanism, accessibility implementation and test approach, form-factor handling, fidelity to the prototype |
| 10 | Identity, Access & Tenancy | Identity provider, flows per surface (browser vs native vs desktop), roles & permissions model, tenancy model & isolation, session/token lifetime and storage per platform, admin/impersonation, API client auth |
| 11 | Data Management & Privacy | Stores per bounded context, retention & deletion, PII inventory & classification, consent, backup/restore & RPO/RTO, import/migration of legacy data, export/portability, data residency |
| 12 | Delivery, Environments & Hosting | Environments, CI/CD, branching & versioning, hosting/cloud and cost envelope, store/installer/updater pipelines, feature flags, rollback, signing & secrets |
| 13 | Observability & Operations | Structured logging, metrics, tracing, alerting thresholds, product analytics tracking plan & consent, crash reporting for native clients, support workflow, runbooks, SLA/SLO |
| 14 | Testing Strategy | Test pyramid per BC, BDD scope, E2E & accessibility & visual regression (against the mockups), device/browser/OS matrix, test data, performance tests, definition of done |
| 15 | AI/ML Features *(conditional)* | See gap 15 |

Same rules as existing dimensions: one question at a time, recommendation attached, skipped dimensions recorded as *not applicable*, answers logged to `session-decisions.md`. Quality-attribute answers still land in Dimension 7 and are **not** numbered as acceptance criteria (rule in `traceability.md` unchanged).

### Deliverable 4 — Product Specification

`docs/product/product-specification.md`, written at the end of finalisation (after Deliverables 1–3). An index with substance, one document a stakeholder can read:

1. **What we are building** — vision, problem, audience segments, personas, value, goals & metrics
2. **Scope & release plan** — MoSCoW, MVP, phases, launch & adoption
3. **Experience** — journeys, screen inventory (`SCR-`), UX & UI principles, accessibility & localisation targets, **links to wireframes, mockups and the clickable prototype**, validation-log summary
4. **Surfaces & deliverables** — final deliverables register per web/mobile/desktop/other, distribution and update channel
5. **Domain** — bounded contexts, glossary link, use-case and story index
6. **Technical requirements** — architecture summary + ADR links; Dimensions 9–15 decisions; Dimension 7 quality attributes as measurable numbers; constraints and forbidden-tech check result
7. **Compliance register**
8. **Roadmap & rough sizing** with the scope-vs-budget verdict
9. **Traceability matrix** — goal → capability → screen / use case / story (`SCR-`, `UC-`, `US-`) → surface → architecture decision; uncovered goals listed
10. **Risks, assumptions, deferred decisions, open questions** — merged from both interviews, each with owner and validation date
11. **Sign-off** — who confirmed, when

Skip rule is unchanged: a deliverable may be skipped only with explicit consent and is recorded as Deferred in the closing summary.

## Gap register (self-review of this plan)

| # | Gap found in revisions 1–2 | Closed by |
|---|---|---|
| G1 | No mocks, mockups or clickable demos | *Mocks, mockups and clickable prototype*, Phases 8/9/11, `prototype/` outputs, `prototype-guide.md`, scaffold |
| G2 | Respondent only sees text; no feedback loop on visuals | Show-back rounds at wireframe, mockup and prototype level |
| G3 | "My recommendation" on factual questions would anchor the answer | Recommendations for decisions only; facts asked neutrally |
| G4 | Only greenfield was covered | Product-type fork (new / extension / replacement / internal / platform) |
| G5 | No stakeholder map or decision rights | Phase 0 governance, sign-off by the decision owner |
| G6 | No product name / branding / domain | Phase 0 |
| G7 | No monetisation, payments, tax, store commercial rules | Phase 6 |
| G8 | No launch, pilot, adoption or training | Phase 15 |
| G9 | No AI/ML coverage | Phase 7 sub-block, Dimension 15 |
| G10 | No content strategy, notifications, e-mail, help centre, legal text ownership | Phase 8, `ux-brief.md` inventory |
| G11 | No measurement plan tying metrics to instrumentation | Phase 4 → tracking plan in Dimension 13 |
| G12 | No import/bulk, moderation, user-generated content | Phase 7 |
| G13 | No legal/consent documents, DPIA, open-source obligations | Phase 13 |
| G14 | No feasibility check against budget and team | Product Specification roadmap & sizing |
| G15 | Interrupted sessions would lose context | Resumable logs in both skills |
| G16 | Confidential data and personas with real people | Confidentiality rule, fictional personas |
| G17 | Mocks could depict things that cannot be built | Built-only-from-existing-components rule, `custom` flag |
| G18 | Build could drift from the approved design | Dimension 9 prototype fidelity, visual-regression baseline |
| G19 | Prototype could be mistaken for the product or leak | Visible "prototype" label, no real data/services, local-first, publishing only on request |
| G20 | Skill description would not trigger for Dutch speakers | English + Dutch trigger phrases |
| G21 | Plan edited `.ai/ai.json`, which is gitignored/generated | Removed from the files-touched list |
| G22 | No tests of the skill itself | Step 9: trigger test, eval cases via `skill-creator`, dry runs |
| G23 | Council triggers could be missed | Gap 17 |
| G24 | Discovery IDs might collide with traceability IDs | Own prefixes; verified against validator regexes at step 1 |
| G25 | Respondent must compose answers from scratch; heavy for customers | *Answer ergonomics*: multiple choice by default, curated option sets, pre-filled answers, batching, free input always available |
| G26 | Choice sets larger than the tool's 4 options (languages, integrations, devices) | Two-step choice or multi-select over the likeliest items plus *Other* |
| G27 | Visual decisions are hard to choose from words | Option previews and fixed reaction sets for mocks |
| G28 | Clients without a choice tool (Copilot, Reasonix) | Lettered-list fallback with the same parsing |
| G29 | Respondent forced to answer when unsure | *Not sure yet / Decide later / Not applicable* escape options mapped to Assumption / Deferred / N-A |

## Files touched

| File | Change |
|---|---|
| `.ai/skills/product-discovery/SKILL.md` | New |
| `.ai/skills/product-discovery/references/{question-bank,output-templates,prototype-guide}.md` | New |
| `.ai/skills/product-discovery/assets/prototype-scaffold/` | New (HTML/CSS/JS shell, no build step, no external dependencies) |
| `.ai/skills/design-interrogation/SKILL.md` | Extended per gap table |
| `.ai/reference/work-type-mapping.md` | Add *Product Discovery* row; extend *Design Interrogation* row |
| `.github/copilot-instructions.md` | Same mapping rows (confirm whether generated) |
| `README.md` | Skills table, pipeline/usage section, file structure, work-type mapping, skill count if stated |
| `TEMPLATE-FAQ.md`, `TEMPLATE-USAGE.md` | Slash-command list; pipeline description begins with discovery |
| `.ai/tests/validate-upgrade-script.py` | Add new skill path to the expected-files list; extend the pipeline-connectivity test |
| `.ai/reference/traceability.md` | Only if a note on the non-validated discovery prefixes is warranted |

Not touched: `.ai/ai.json` (gitignored, generated), `CHANGELOG.md` (written by CI), `.ai/session-context.md` (this repo is the template and ships it as an unfilled placeholder). Junctions need no per-skill change; `sync-platforms` is run to confirm no drift.

## Steps

1. Re-search the solution for existing `product-discovery` / `product-brief` / `prototype` / persona assets; read `traceability.md`, `validate-skills.py`, `validate-references.sh`, `validate-tokens.sh`, `validate-triggers.py`, `validate-content.py`, `validate-prose.py` for constraints on skill sub-files (`references/`, `assets/`), token budgets and trigger clauses; read `css-theme-generator` and the `ui-*` skills for token/component facts. *(Explore)*
2. Design the prototype scaffold and write `references/prototype-guide.md` and `assets/prototype-scaffold/`. *(designer + ui-developer)*
3. Draft `references/question-bank.md` (including the option set for every question) and `references/output-templates.md`. *(writer, using `skill-creator`)*
4. Draft `product-discovery/SKILL.md`; optimise the `description` for trigger accuracy in English and Dutch ("interview me", "new product", "product idea", "requirements", "discovery", "what should we build", "PRD", "mockup", "clickable demo", "interview mij", "nieuw product"). *(writer, using `skill-creator`)*
5. Extend `design-interrogation/SKILL.md` per the gap table (gaps 1–21). *(writer)*
6. Wire in `work-type-mapping.md`, `copilot-instructions.md`, `validate-upgrade-script.py`. *(developer)*
7. Update `README.md`, `TEMPLATE-FAQ.md`, `TEMPLATE-USAGE.md` per `.ai/reference/readme-maintenance.md`. *(writer)*
8. Run `sync-platforms` and the full validation suite (`.ai/tests/validate-*`, `smoke-test.py`, `hygiene-lint.py`); fix findings.
9. Test the skill: answer-ergonomics check (every question has an option set or a stated reason for being free text; no choice question lacks free input; option counts within 2–4; lettered fallback renders); trigger test on 10 should/should-not prompts; dry-run interviews against one sample product per respondent mode (customer, product owner, developer) producing all documents and a working prototype; verify the prototype with `ui-tester` (navigation, states, contrast, keyboard, offline); verify `design-interrogation` imports `PD-` items without re-asking and produces the Product Specification. *(tester, ui-tester)*
10. Independent review of both skills: coverage against the phase table and gap register, no contradiction with existing rules, Dimension 1–8 numbering intact. *(reviewer)*
11. Update `README.md` for the change (closing step), mark progress DONE, move to `.ai/completed/`.

## Verification

- All repository validators pass; no sync drift.
- `design-interrogation` still reads end to end without orphaned references to "three deliverables" or "Dimensions 1–8".
- Sample run produces: six discovery documents, a prototype that opens from the file system and completes every top journey, a populated `session-decisions.md` with `PD-` sources, and a Product Specification whose traceability matrix lists any goal without a use case or screen.

## Risks

0. **Choice sets bias answers or hide the real one** — mitigated by *Other* on every question, recommendations only for decisions, neutral option order for fact questions, and verbatim recording of typed answers.

1. **Interview fatigue** — 18 phases (0–17) is long. Mitigation: skip logic, role-based depth, playback checkpoints, show-back rounds that re-engage the respondent, and resumable capture so it can run over several sessions; Customer mode covers phases 1–9, 11, 13 and 15 (always including the audience and the prototype) and leaves the rest to a technical colleague.
2. **Prototype effort and scope creep** — a prototype can swallow the interview. Mitigation: fidelity levels limited to top journeys, scaffold with toggles instead of bespoke code, and an explicit rule that the prototype is a communication tool, not the product.
3. **Skill size / token budget** — mitigated by moving question lists and the prototype guide to `references/`, the scaffold to `assets/`; step 1 confirms the validators allow it.
4. **Two skills overlap on Purpose & Scope** — mitigated by the pre-resolved import: `design-interrogation` never re-asks what `PD-` already resolved.
5. **Over-prescribing stack** — discovery asks about outcomes and constraints; stack choices stay in `design-interrogation` and default to the template's `tech-stack.md`.
6. **Mocks mistaken for commitments** — mitigated by the prototype label, the `custom` flags, and the Product Specification stating what the prototype does and does not promise.
