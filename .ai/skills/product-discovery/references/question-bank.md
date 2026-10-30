# Product Discovery — Question Bank & Option Sets

**Load only the section for the current phase — do not read this whole file.**

Reference for all questions per phase (0–17) with curated option sets, decision mappings, escape routes, and reaction templates. Translate questions to the respondent's language; instruct the skill: *"Questions appear in English; answer in your language. If you'd like the question rephrased, say so."*

**Question Modes** (every question carries one):
- `Mode: choice` → Answer via `AskUserQuestion` with listed options (single or multi-select). Fallback for clients without choice tools: lettered list (A, B, C, …).
- `Mode: text` → Plain chat prompt; batched up to 4 per round into one numbered message. Respondent answers by number (1), (2), etc.

**Escape Options** (offered when applicable, always NOT counted in the 4-option limit):
- *Not sure yet* → Assumption (flag decision, name validation method)
- *Decide later* → Deferred (name owner, target date)
- *Not applicable* → N/A (skip question or section)

**Answer Ergonomics:**
- Every choice question offers *Other* (free input always available).
- Recommendations appear only on **decisions**, never on **facts**. Facts are asked neutrally.
- Pre-filled answers from documents/tech-stack.md labelled *(from {source})* and marked as the first option for confirmation with one click.
- Visual choices include ASCII preview or rendered sample so the respondent compares, not imagines.
- Larger option sets (languages, countries, devices, integrations): two-step choice (group → items) or multi-select over the 4 likeliest items + *Other*.
- Free text questions marked `free text` with reason.
- Every answer is checked for: **number** (where a number is possible), **named owner** (for decisions/tasks), **example** (when vague), **exception** (when broad). Missing triggers a follow-up before the phase closes.

**Progress line each round:** *Phase N of 18 — {topic}, about X rounds left.*

**Playback checkpoints** (every phase): 3–5 line summary; respondent confirms or corrects.

---

## Phase 0 — Intake, Respondent & Governance

**Rounds:** 5 rounds



### 0.1 — Respondent Mode
- **Header:** Mode
- **Mode:** choice
- **Question:** Which role best describes you? This changes the depth and vocabulary, never the coverage.
- **Options:**
  - *Developer* — I write and ship code, familiar with architecture, CQRS, aggregates.
  - *Product Owner* — I define features, goals, and customer needs; I drive prioritisation.
  - *Customer / Business Stakeholder* — I know the problem and the outcome wanted; I may not know technology details. (Use *[TECH-OPEN]* in outputs for technical gaps I cannot answer.)
  - *Mixed* — Multiple people will answer; please name them and their roles in the next question.
- **Escape options:** None.
- **Customer mode rewrite:** Same.
- **Developer mode terse:** Mode (Dev / PO / Cust / Mixed).
- **Mapping:** Sets vocabulary depth and role-aware tone for all subsequent questions.
- **Example:** "I'm a product owner, but I'll bring our lead developer to Phases 8, 9, 10 and 12 for technical calls."

### 0.2 — Team & Decision Rights
- **Header:** Who decides
- **Mode:** text
- **Question:** Who has final sign-off on **scope**, **design decisions**, and **budget**? Name them; if they differ per area, say so. (This prevents later conflicts.)
- **Options:** `free text` — Names, roles, and who decides what. Reason: Unique per organisation.
- **Example:** "Sarah (CEO) signs scope and budget; Tom (Design Lead) approves UI; I (PM) drive daily calls."
- **Escape:** *Not sure yet* → Assumption (will confirm in Phase 17).
- **Follow-up rule:** Must have at least one name per area (scope, design, budget). If vague, ask: "Who would you call if design takes longer than expected?"

### 0.3 — Product Type Fork (Origin & Orientation)
- **Header:** Type
- **Mode:** choice
- **Question (Step 1 — Origin):** Are you building something new, extending an existing product, or replacing a legacy system?
- **Options:**
  - *New product (greenfield)* — Building from scratch; no legacy, no existing users.
  - *Extending an existing product* — New features in a product already in the market; existing users, design system, codebase.
  - *Replacement / migration* — Replacing an old system; must preserve some behaviour, migrate data.
- **Multi-select:** No.
- **Question (Step 2 — Orientation):** Who is this for? (Single select.)
- **Options:**
  - *Internal tool* — Built for your staff, not customers; density and keyboard matter; support is in-house.
  - *Customer-facing* — Sold or distributed to external customers or users.
  - *Platform / API / SDK* — Built for other developers; developer experience, docs, and client libraries matter most.
- **Mapping:** Origin activates skip logic: *Extending* → Phase 0 reads existing docs/screenshots/Figma; Phases 2 and 9 become "confirm and amend" (codebase-read and existing-UI inventory inform these phases). *Replacement* → Phase 1 expanded (add 1.4 current-system pain points, 1.5 must-keep behaviour); Phase 12 adds migration questions, Phase 15 adds switch-over question. Orientation → Phase 2/8/9 density, Phase 7 API/SDK focus, Phase 8/9 keyboard emphasis for internal.
- **Example:** "New product (greenfield) for a logistics-yard app. Customer-facing (sold to small yards). We're also building a web dashboard for ops; that's a second product (new, internal tool)."

### 0.4 — Existing Documents & Assets
- **Header:** Input
- **Mode:** text
- **Question:** Do you have documents, screenshots, Figma links, or other research on this product? (Saved to `docs/input/` so we can read them.)
- **Options:** `free text` — File names, Figma links, or *None yet*. Reason: Unique paths per project.
- **Example:** "Figma: https://figma.com/file/xyz; analytics_report_2026q3.pdf; user_interviews_sept.txt"
- **Escape:** *None yet* → Proceed; assume zero prior research.

### 0.5 — Product Name & Domain
- **Header:** Name
- **Mode:** text
- **Question:** What is the product called? Include domain/website if the company exists.
- **Options:** `free text` — Product name + optional domain/trademark status. Reason: Unique per project.
- **Example:** "Yardie Logistics (internal codename). Domain: yardie.com not yet registered; no trademark search done."
- **Escape:** *Not yet decided* → Assumption (will confirm in Phase 17).

### 0.6 — AI/ML Features Present?
- **Header:** AI?
- **Mode:** choice
- **Question:** Does this product include AI or machine-learning features? [TECH-OPEN if yes]
- **Options:**
  - *No, not planned* — No AI/ML
  - *Possibly, not yet decided* → Deferred; owner named in follow-up; enables Phase 7 AI sub-block on resume.
  - *Yes, but I'm still exploring* → Assumption; Phase 7 AI sub-block on this session; Phase 7 deep-dive focuses on use, data, cost, safety.
  - *Yes, requirements defined* → Phase 7 AI sub-block with existing constraints pre-filled.
- **Escape options:** Not sure yet → Assumption (will validate); Decide later → Deferred (owner named).
- **Mapping note:** If *Possibly* or *Yes*, Phase 7 expands with the AI sub-block; if *No*, skip it.
- **Mapping:** Activates Phase 7 AI sub-block (conditional); gates Dimension 15 in design-interrogation.
- **Example:** "Yes, but early-stage. We're looking at route-optimisation (nearest-depot algorithm) and predictive ETA."

### 0.7 — Stakeholder Map
- **Header:** Stakeholders
- **Mode:** text
- **Question:** Who else must be heard during this interview? (Whose voices would change the answer?)
- **Options:** `free text` — Names, roles, decision areas (e.g., "Sarah (CEO, approves scope); Tom (Design lead, UI decisions); Priya (compliance officer, legal risk)"). Reason: Unique per organisation.
- **Example:** "Sarah (CEO, scope + budget approval). Tom (Design lead, UI/UX). Priya (compliance, legal/GDPR). Dev team lead (can join technical phases 10–14, optional)."
- **Escape:** *Not sure yet* → Assumption (will confirm in Phase 17).
- **Follow-up rule:** For each stakeholder: when can they join, which phases are critical for them?
- **Mapping:** Informs Phase 0.2 (decision rights); shapes session planning (who attends which phases).

### 0.8 — Existing UI Inventory (If Extending)
- **Header:** Current UI
- **Mode:** text
- **Question (Conditional: asked only if Phase 0.3 Origin = *Extending*):** Do you have screenshots, Figma files, or a live product we should inspect? (We will read the existing design before asking you to confirm or amend the brand, audience, and UX.)
- **Options:** `free text` — Figma link, screenshot folder, live product URL, design-system docs. Reason: Varies per product.
- **Example:** "Figma: https://figma.com/file/xyz (shared, can read). Live product: staging.company.com (login: test@example.com). Design system: in Figma under 'Components'."
- **Escape:** *None yet* → Proceed; assume no prior UI artefacts.
- **Mapping:** Skill reads the inventory before Phase 2 (audience); Phase 9 (UI) will "confirm and amend" existing design system instead of starting from scratch.

---

## Phase 1 — Problem & Opportunity

**Rounds:** 2 rounds



### 1.1 — Problem Statement
- **Header:** Problem
- **Mode:** text
- **Question:** What problem does this product solve? For whom? Why is it urgent *now*?
- **Options:** `free text` — Problem statement, customer segment (rough), reason for timing. Reason: Each product has a unique problem narrative.
- **Follow-up rule:** Look for: problem owner (who has it), magnitude (cost/impact), timing trigger (why now). Missing any? Ask follow-ups before leaving the phase.
- **Example:** "Logistics yards waste 20% of staff time on manual vehicle-dispatch spreadsheets. Mobile devices are standard now (2026), so a native app is feasible. Current vendor's SaaS is locked to desktop."
- **Customer mode rewrite:** Same.
- **Developer mode terse:** Problem, who owns it, cost, timing trigger.
- **Mapping:** PD-001 (Resolves problem scope; constrains Phases 2–5).

### 1.2 — Today's Workaround (How is it solved now?)
- **Header:** Today
- **Mode:** text
- **Question:** How do people solve this problem today? (Spreadsheets, a vendor tool, manual process, something else?)
- **Options:** `free text` — Current workaround + pain points. Reason: Varies per domain.
- **Example:** "Dispatch manager uses Google Sheets + phone calls. Takes 45 min per day; drivers don't see routes until they call in. No history; every yard manager invents their own process."
- **Mapping:** Informs Phase 6 (competitive landscape); Phase 7 (current workflows to improve).

### 1.3 — Cost of Not Solving
- **Header:** Cost
- **Mode:** text
- **Question:** What does inaction cost? (Lost productivity, lost customers, compliance risk, etc.)
- **Options:** `free text` — Annual cost, frequency, or risk if vague. Reason: Unique per problem.
- **Follow-up rule:** If not a number, ask: "How many hours per day?" or "How much revenue at risk?"
- **Example:** "£4,000/month in wasted labour (20% of 2 dispatchers × 4 yards). Lost bids if we can't dispatch fast. Yard managers waste 10 hours/week on coordination."

### 1.4 — Current-System Pain Points (If Replacement or Extension)
- **Header:** Pains
- **Mode:** text
- **Question (Conditional: asked if Phase 0.3 Origin = *Replacement* or *Extending*):** What frustrates you most about the current system? (What must the new product improve?)
- **Options:** `free text` — Pain list (e.g., "slow UI, unreliable syncing, no mobile, poor reports, vendor lock-in, unsupported OS"). Reason: Varies per system.
- **Example:** "Dispatch system is 15-year-old desktop-only app. No mobile support. Syncing takes 10 minutes (unacceptable in field). UI is confusing; staff needs training every time there's a change. Vendor is unresponsive; feature requests get no reply."
- **Escape:** *Not sure yet* → Assumption; ask the team to list pains before Phase 2.
- **Mapping:** Constrains Phase 5 (must-haves in scope); Phase 1.5 identifies what to keep.

### 1.5 — Must-Keep Behaviour (If Replacement or Extension)
- **Header:** Must-keep
- **Mode:** text
- **Question (Conditional: asked if Phase 0.3 Origin = *Replacement* or *Extending*):** What about the current system *must* the new product preserve? (What workflows are you not willing to lose?)
- **Options:** `free text` — Behaviour list (e.g., "keyboard shortcuts for power users, CSV export format, integration with X, specific calculations, UI patterns familiar to staff"). Reason: Varies per system.
- **Example:** "Power users rely on 5 keyboard shortcuts (must stay). Dispatch history must export to Excel in the same format (existing reports depend on it). Integration with payroll system must not break. Field crews are used to the 'all day' view (plan the whole day at a glance)."
- **Escape:** *Nothing* → Greenfield approach; no backwards-compat needed.
- **Mapping:** Constrains Phase 8 (UX/navigation) and Phase 5 (MVP must include these); Phase 12 (data migration and integration).

---

## Phase 2 — Audience

Asked early because it drives UX, UI, and platform defaults. Asked for **every segment** (primary, secondary, tertiary, ranked).

**Rounds:** 4 rounds + 1 confirmation (one repeat per segment); Phase 2 loop rule: ask segment 1 fully (all 11 areas), then for further segments ask only the areas that differ, offering 'Same as segment N' as first option.

**Intro:** We're mapping who uses this product. Each answer will shape the design and platforms. Let's go segment by segment.

**Core Questions:**

### 2.1 — Audience Type & Segmentation
- **Header:** Who
- **Mode:** choice
- **Question (Step 1):** Who is your primary customer group?
- **Options:**
  - *B2C (consumers)* — Individual end users
  - *B2B (business customers)* — Companies or departments as customers
  - *B2E (internal staff)* — Our own employees or partners' staff
  - *B2G (government / public)* — Citizens or government bodies
- **Question (Step 2):** Who else uses it? (Multi-select; secondary/tertiary groups.)
- **Options (multi-select, max 4):**
  - *B2C (consumers)* — Individual end users
  - *B2B (business customers)* — Companies or departments as customers
  - *B2E (internal staff)* — Our own employees or partners' staff
  - *B2G (government / public)* — Citizens or government bodies
- **Escape options:** *B2D (developers / partners)*, *Other segment types* (free text).
- **Multi-select:** Step 2 yes; Step 1 primary single-select, order derived from answers.
- **Follow-up rule:** For each segment, ask: how many now? growth in 3 years? who *buys* vs who *uses* vs who *decides*?
- **Example:** "Primary: dispatch managers (4 now, 12 in 3 years; they buy and use). Secondary: drivers (20 now, 60 in 3 years; use only, manager decides). Tertiary: admin (2 now, 4 in 3 years; use for reporting)."
- **Mapping:** SEG-001, SEG-002, SEG-003 (each segment gets an ID); constrains all following Phase 2 questions per segment.

### 2.2 — Demographics (per segment)
- **Header:** Demographics
- **Mode:** text
- **Question:** For [{segment}]: age range, profession/role, education, income (if it affects pricing/messaging)?
- **Options:** `free text` — Age range, title, education level. Reason: Varies per segment.
- **Example:** "Dispatch managers: 28–55, logistics supervisors / yard managers, high-school or diploma. Income band: £30–60k (not a pricing driver; affects affordability messaging in onboarding)."
- **Mapping:** Constrains typography (reading level), tone, imagery, pricing messaging.

### 2.3 — Geography, Language, Cultural
- **Header:** Geography
- **Mode:** text
- **Question:** For [{segment}]: countries/regions, languages spoken, reading level, cultural conventions (colour, date/number formats, RTL, taboos)?
- **Options:** `free text` — Countries, languages, reading level (plain English, technical jargon OK, non-native needs support), date format, RTL. Reason: Unique per segment.
- **Follow-up rule:** If multiple languages, ask: which is primary? which will the product launch in? (Rest are deferred.)
- **Example:** "Dispatch managers: UK-based, English only, reading level plain English, no technical jargon. Date format: DD/MM/YYYY (UK standard). No RTL, no colour taboos."
- **Mapping:** Constrains Phase 8 (content tone), Phase 9 (typography, layout, localisation scope in Phase 10), Phase 13 (legal region for T&Cs, privacy, data residency in Phase 12).

### 2.4 — Digital Skill & Habits
- **Header:** Skills
- **Mode:** choice
- **Question:** For [{segment}]: how tech-savvy? Familiar with comparable products? Apps they use daily?
- **Options:**
  - *Power user* — Very comfortable with tech; familiar with multiple SaaS tools; expects shortcuts and advanced features.
  - *Proficient* — Comfortable with common tools (Slack, Gmail, spreadsheets); willing to learn a new interface if it saves time; moderate onboarding tolerance (10–20 min).
  - *Learning / casual* — Uses basic tools; needs guidance and clear labelling; longer onboarding (30+ min) acceptable if trained.
  - *Not tech-focused* — Prefers simplicity; learns through hands-on; impatient with complex workflows; needs support.
- **Escape options:** *Not sure* → Assume middle ground (Proficient); validate in Phase 11.
- **Follow-up rule:** Comparable products they know? (This sets expectations for features and UX patterns.) Daily apps they rely on? (e.g., Slack, WhatsApp, Gmail — what UI patterns do they expect?)
- **Example:** "Dispatch managers: Proficient. Use Slack, Gmail, Google Sheets daily. Familiar with one SaaS dispatch tool from previous jobs. Will spend 20 min on onboarding if it saves time daily."
- **Mapping:** Constrains Phase 8 (onboarding depth, progressive disclosure), Phase 9 (animation / micro-interactions — reduced for focused work), Phase 5 (MVP must include features they know to expect).

### 2.5 — Devices & Connectivity
- **Header:** Devices
- **Mode:** choice
- **Question (Step 1):** For [{segment}]: what's their connectivity like?
- **Options:**
  - *Always online* — Desk-based; WiFi reliable; can use cloud-only (no offline needed).
  - *Mixed (mostly online)* — Office + field; both WiFi and mobile 4G; occasional offline periods; sync-on-resume acceptable.
  - *Often offline* — Field work; sporadic WiFi; mobile data unreliable; local-first, sync-on-reconnect required.
- **Question (Step 2):** Which devices do they use? (Multi-select of 4 likeliest.)
- **Options (multi-select):**
  - *Smartphone* — iPhones, Android phones; primary mobile device.
  - *Tablet* — iPads, Android tablets; larger screen.
  - *Desktop/laptop* — Windows, Mac, Linux; stationary work.
  - *Shared/kiosk* — Shared device; limited personal customisation.
- **Escape options:** *Other* → Older hardware versions, other form factors (free text with details).
- **OS/browser mix (free text follow-up):** Version specifics (e.g., "iOS 16+, Android 11+, Windows 10/11, Chrome/Edge/Safari"). Reason: Varies per segment.
- **Example:** "Dispatch managers: always online (office-based). Devices: iPhone 12/13 (iOS 16+), shared iPad, Windows laptops (Chrome, Edge). Never offline."
- **Mapping:** Constrains Phase 10 (web vs iOS vs Android vs desktop), Phase 8 (responsive breakpoints: phone, tablet, desktop), Phase 13 (device storage, sync-conflict policy).
- **Escape option:** *Too varied* → Proceed with top 3 devices; confirm coverage in Phase 17.

### 2.6 — Context of Use & Interruptions
- **Header:** Context
- **Mode:** choice
- **Question (Step 1):** For [{segment}]: where and when do they use this?
- **Options:**
  - *Office/desk* — Stationary, reliable environment (light, power, internet); continuous focus possible.
  - *Field/mobile* — Outdoors, moving, variable conditions (bright light, no power, spotty WiFi, interruptions).
  - *Mixed (office + field)* — Both; must adapt to both contexts.
- **Question (Step 2):** How often are they interrupted while using it?
- **Options:**
  - *Rare* — Can focus; expects features, depth, no rushing.
  - *Occasional* — Some breaks; expects to save state mid-task and resume.
  - *Frequent* — Many interruptions (radio, phone calls, people stopping by); expect quick actions (2–10 min), no long workflows.
- **Follow-up rule:** Single-handed use needed? (This affects touch target size and layout.)
- **Example:** "Dispatch managers: Mostly office-based. Frequent interruptions (radio, phones, drivers dropping by). Sessions 2–10 min, 20+ times/day. Occasionally one-handed (holding radio). High ambient light in yard."
- **Mapping:** Constrains Phase 8 (session-awareness: save state mid-journey, quick-load time, no long workflows), Phase 9 (touch target size ≥48px for frequent interruptions, single-handed reachability, high-contrast for outdoor light).

### 2.7 — Accessibility & Legal Obligations
- **Header:** A11y
- **Mode:** choice
- **Question:** For [{segment}]: share with visual, hearing, motor, cognitive needs? Screen-reader / zoom / voice / switch / reduced-motion use? Colour-blindness? Legal obligation (WCAG level, EN 301 549, EAA)?
- **Options:**
  - *Low accessibility need; no legal duty* — <5% users likely need accommodations; WCAG A sufficient.
  - *Moderate need or legal duty* — 10–20% users; WCAG AA (industry standard); some may use screen reader or zoom.
  - *High need or strict legal duty* — >20% or legally mandated (e.g., EN 301 549 for EU public services); WCAG AAA or AA+; assistive-tech test matrix required.
  - *Unknown; will research* → Assumption; Phase 13 adds accessibility legal review.
- **Escape options:** Not sure → Assume WCAG AA (safe default; improves usability for all); decide later with Phase 13 legal review.
- **Follow-up rule:** If legal duty stated, ask: "Which jurisdiction? Which standard (WCAG, EN 301 549, EAA)?" Record in Phase 13. For high need: what assistive tech do they use?
- **Example:** "Dispatch managers: No legal duty stated. Estimated <5% accessibility need. Target WCAG AA (shows respect; improves usability for all, e.g. focus indicators for keyboard users)."
- **Mapping:** Constrains Phase 9 (colour + contrast pairs checked against WCAG level before mockup show-back), Phase 8 (focus order, labels, keyboard navigation), Phase 10 (testing matrix in Platform Deliverables), Phase 13 (legal review of accessibility requirements).

### 2.8 — Motivation, Emotion & Trust
- **Header:** Emotion
- **Mode:** text
- **Question:** For [{segment}]: why do they come? What frustrates them *today*? stress level of the task (e.g., payments, health, logistics delay)? desired feeling (calm, playful, fast, authoritative, premium)?
- **Options:** `free text` — Motivation, current frustrations, stress level (high, medium, low), desired tone (calm, playful, fast, formal, friendly). Reason: Varies per segment.
- **Example:** "Dispatch managers: Come to save time and reduce errors. Frustrated by spreadsheet chaos, driver confusion, slow updates. High stress (delays = customer complaints). Desired tone: fast, clear, professional (not playful)."
- **Mapping:** Constrains Phase 9 (tone of voice, visual mood: calm/energetic/formal), Phase 8 (feature priority: speed over features; happy-path urgency).
- **Bias guard:** Questions avoid solutioneering ("should it be an app?") before the problem and audience are settled.

### 2.9 — Brand Fit & Voice
- **Header:** Brand
- **Mode:** text
- **Question:** For [{segment}]: formal vs informal address? humour allowed? brand personality? competitors' look they want to resemble or avoid?
- **Options:** `free text` — Formality (formal / casual / friendly), humour tolerance (yes / no / situational), brand words (e.g., "professional, transparent, playful"), competitors they admire or dislike. Reason: Varies per segment.
- **Example:** "Dispatch managers: Formal address (Mr/Ms convention). No humour in UI (they're stressed). Brand: 'professional, reliable, no-nonsense.' They like Slack's clean look; avoid TikTok vibe."
- **Mapping:** Constrains Phase 9 (typography choice, illustration style, colour mood, copy tone).

### 2.10 — Access, Safeguarding, Minors
- **Header:** Safety
- **Mode:** choice
- **Question:** For [{segment}]: minors involved? vulnerable people? consent/guardianship rules? safety-critical use?
- **Options:**
  - *Adults only; no safety concerns* — All users are 18+; no vulnerable people; non-critical use (delays are inconvenient, not dangerous).
  - *Minors; parental consent required* → Parental consent flows, data minimisation, content moderation required in Phase 13.
  - *Vulnerable people; duty of care applies* → Safeguarding rules, simplified UX, human oversight required in Phase 13.
  - *Safety-critical (health, driving, finance)* → Error tolerance, undo, reassurance copy, compliance required in Phase 13.
- **Escape options:** *Not sure yet* → Assumption; Phase 13 reviews.
- **Example:** "Dispatch managers: All adults. Not safety-critical (logistics delay, not life/death). Drivers are also adults. No minors or vulnerable people."
- **Mapping:** Constrains Phase 13 (consent rules, moderation, duty-of-care rules, undo/reassurance copy, safety-critical compliance).

### 2.11 — Evidence & Research
- **Header:** Evidence
- **Mode:** text
- **Question:** For [{segment}]: what evidence exists? (user research, analytics, support tickets, interviews, surveys, personas). What is known vs guessed?
- **Options:** `free text` — Research type (interviews, surveys, analytics logs, personas, support tickets), sample size, date, known-vs-guessed breakdown. Reason: Varies per project.
- **Example:** "5 dispatch managers interviewed Sept 2026 (known). 20 user support tickets mentioning 'slow updates' (known). Estimated 20% growth in 3 years (guessed; no market data)."
- **Follow-up rule:** For guesses, ask: "How confident? What would validate this?" Record in Phase 16 (Risks, Assumptions, Dependencies).
- **Mapping:** Guesses logged as Assumptions to validate; known data used for confident design decisions in Phase 9.

**Audience → Design Traceability:** See the canonical audience-profile-template in `output-templates.md` for the traceability table (which designs each audience finding constrains). This table is the single source of truth for design decisions downstream in Phases 8–10.

---

## Phase 3 — Users & Personas

**Rounds:** 2 rounds (per persona)



### 3.1 — Primary Users & Jobs-to-be-Done
- **Header:** Users
- **Mode:** text
- **Question:** For [{segment}], who are the primary users? What are their main jobs/tasks? (E.g., "Alice: dispatch manager, daily task is assigning routes.")
- **Options:** `free text` — Persona name, role, main task/job. Reason: Unique per product.
- **Follow-up rule:** For each persona, capture: name, role, primary job (1–2 sentences). Example persona names: factual, fictional composites, not real people.
- **Example:** "Alice: Dispatch manager, 15 years in logistics. Primary job: assign drivers to routes each morning, ~45 min."
- **Mapping:** Creates persona IDs reused by Phase 8 (journeys) and user-story skill ("As {persona}...").

### 3.2 — Secondary & Support Users
- **Header:** Support
- **Mode:** text
- **Question:** Are there secondary users or support roles? (E.g., admins, auditors, support staff.)
- **Options:** `free text` — Role, name, interaction frequency (daily, weekly, monthly). Reason: Varies per product.
- **Example:** "Bob: Admin, weekly; sets up drivers and zones. Charlie: Operations Lead, daily; approves bulk route changes."

### 3.3 — Context of Use (per persona)
- **Header:** Use context
- **Mode:** text
- **Question:** For [{persona}]: where/when do they use the product? Desk, field, both? Interruptions? Session length?
- **Options:** `free text` — Context (desk, field, both), interruptions (frequent, occasional, rare), session length (5 min, 30 min, all day). Reason: Varies per persona.
- **Note:** Phase 2 asks this for the segment; Phase 3 confirms per persona. If identical, say "same as {segment}."
- **Example:** "Alice: Mostly desk, some field (checking on stranded drivers). Frequent interruptions (radio, phones). Sessions 2–10 min, 20+ times/day."

---

## Phase 4 — Value & Success

**Rounds:** 2 rounds



### 4.1 — Value Proposition (per segment)
- **Header:** Value
- **Mode:** text
- **Question:** For [{segment}], what is the value? (Time saved, revenue gained, risk reduced, ease of use, trust, compliance.)
- **Options:** `free text` — Value statement + metric (hours saved/day, £ revenue, %, % improvement). Reason: Unique per segment.
- **Follow-up rule:** Look for a quantified metric. If vague ("easier"), ask: "How much easier? Hours saved? Accuracy improvement?"
- **Example:** "Dispatch managers: 10 hours/week saved. 5% faster route assignment. Drivers see routes in real-time (vs. phone calls). Error rate drops from 8% to <2%."

### 4.2 — Business Goals & KPIs
- **Header:** Goals
- **Mode:** text
- **Question:** What are the business goals for this product? (Revenue, users, retention, cost savings, time-to-market, brand.) For each, state the metric and success number (e.g., "1M users by Q4" or "£100k savings/year").
- **Options:** `free text` — Goal, metric, target number, timeline. Reason: Unique per product.
- **Follow-up rule:** Every goal needs: a metric with a number, a named owner (who tracks it?), and a validation method (how is it measured?). Missing any? Ask follow-ups.
- **Example:** "GL-001: 80% of yard managers using the app by Q2 2027 (measured: login analytics). GL-002: 10 hours/week saved per manager (measured: time-tracking survey). GL-003: 15% reduction in routing errors (measured: support tickets)."

### 4.3 — How Each Metric Will Be Measured (Tracking Plan Seed)
- **Header:** Tracking
- **Mode:** text
- **Question:** For each goal/metric above, how will you measure it? (Analytics event, survey, support tickets, database query, manual count?)
- **Options:** `free text` — Metric name, measurement method (analytics event, survey, logs, manual), frequency (daily, weekly, monthly), owner. Reason: Varies per goal.
- **Note:** This seeds the tracking plan; Dimension 13 (Observability & Operations) in design-interrogation will expand it into instrumentation details.
- **Example:** "GL-001 measured: `app_login` event (daily). GL-002 measured: monthly survey of 10 managers (manual). GL-003 measured: `support_ticket_routing_error` tag (daily, auto)."

### 4.4 — Definition of Done for v1
- **Header:** v1 Done
- **Mode:** text
- **Question:** What must v1 include to be considered done? (E.g., "All primary journeys work, 3 languages, iOS + Android, <5% error rate.")
- **Options:** `free text` — Feature checklist, quality gates (error rate, load time, crash-free %), platform coverage. Reason: Unique per product.
- **Example:** "v1 done: route assignment, driver task list, real-time sync. iOS + Android. English + Dutch. <2% sync errors. <2s load time. No crashes in 100 driver-days of testing."

---

## Phase 5 — Scope & Release Plan

**Rounds:** 3 rounds



### 5.1 — MoSCoW Prioritisation
- **Header:** MoSCoW
- **Mode:** text
- **Question:** List the top 15–20 features/capabilities. For each, mark: **M**ust (core, v1 blocker), **S**hould (high priority, v1 or v1.1), **C**ould (nice-to-have, v2+), **W**on't (explicit out-of-scope, v2 or never).
- **Options:** `free text` — Capability list with Must/Should/Could/Won't labels. Reason: Unique per product.
- **Follow-up rule:** Look for: are the Musts defensible (will v1 launch without them? if yes, move to Should)? Are there Wons (explicit rejections to avoid scope creep later)? Is the team confident in the scope (ask: "Can the team deliver this in {budget/timeline}?").
- **Example:** "M: route assignment, driver list, real-time sync. S: bulk import, performance reports, geofencing. C: predictive ETA, voice updates. W: competitor intel, social-media sharing."

### 5.2 — MVP Boundary & Release Phases
- **Header:** MVP
- **Mode:** text
- **Question:** Which Must/Should capabilities form the MVP? What ships in v1.0, v1.1, v1.2, etc.? Timeline for each release?
- **Options:** `free text` — MVP feature list, release phases (v1.0 Q2 2027, v1.1 Q3 2027, etc.). Reason: Unique per product.
- **Follow-up rule:** Is the MVP small enough to ship in {budget/timeline}? (If no, cut features or adjust timeline. Record the tension in Phase 14: Constraints, Operations & Support.)
- **Example:** "MVP (v1.0, Jun 2027): route assignment, driver list, real-time sync. v1.1 (Sep 2027): bulk import, basic reports. v1.2 (Jan 2028): geofencing."

### 5.3 — Explicit Out-of-Scope
- **Header:** Out-of-scope
- **Mode:** text
- **Question:** What is explicitly *not* in scope for v1 or the product ever? (State to prevent scope creep.)
- **Options:** `free text` — Feature, reason (cost, legal, low priority), when/if it might ship (v2, never, review Q3 2027). Reason: Unique per product.
- **Example:** "Competitor intel (low priority). Predictive ETA (too expensive; revisit Q4 2027). White-label (never; no demand)."

### 5.4 — Kill Criteria
- **Header:** Kill rule
- **Mode:** text
- **Question:** Under what conditions would this product be paused or cancelled? (E.g., "If >10% error rate in beta, or no uptake by Q3 2027.")
- **Options:** `free text` — Kill condition (metric threshold, timeline, market signal), owner (who decides to kill?). Reason: Unique per product.
- **Example:** "Kill if <20% of yard managers use by Q2 2027 (measured: login analytics). Kill if error rate >5% in 30-day beta (measured: support tickets)."

### 5.5 — Provisional Target Surfaces
- **Header:** Surfaces
- **Mode:** choice
- **Question:** Which platforms are we likely to build for? (Multi-select; helps Phase 8/9 show-backs focus on the right surfaces.)
- **Options:**
  - *Web* — Browsers (desktop, tablet, phone); PWA-installable option.
  - *Mobile* — iOS and/or Android; native or web; phone and/or tablet.
  - *Desktop* — Windows and/or macOS; native installers.
  - *Other-API* — API/SDK for third-party integrators.
- **Escape options:** *Other* (custom: kiosk, wearable, embedded, etc.).
- **Mapping:** Phase 8/9 show-backs constrain which wireframes and mockups to produce; Phase 10 finalises the decision.
- **Example:** "Probably web app (internal tool, always online). Maybe mobile later (v1.1). No desktop or API for v1."

---

## Phase 6 — Market & Business Model

**Rounds:** 3 rounds



### 6.1 — Competitive Landscape
- **Header:** Competitors
- **Mode:** text
- **Question:** What products or workarounds compete with this? (Direct competitors, substitutes, the status quo.) What do you do *differently*?
- **Options:** `free text` — Competitor name, what they do, your differentiation (faster, cheaper, better UX, niche focus, integration with X). Reason: Varies per market.
- **Follow-up rule:** Ask: "Screenshots of competitors welcome; what would we copy? What would we reject?"
- **Example:** "Competitors: Samsara (US-based, pricey, overkill for small yards). Google Maps (no dispatch logic). Spreadsheets (our status quo). We: cheaper, local support, no learning curve, offline-first."

### 6.2 — Revenue & Pricing Model
- **Header:** Revenue
- **Mode:** choice
- **Question (Step 1):** How will the product make money?
- **Options:**
  - *Subscription (monthly/annual)* — Recurring revenue; per user, per organisation, or per feature tier.
  - *One-time purchase* — Installer, app store, or perpetual licence.
  - *Freemium* — Free tier + premium upsell.
  - *Other* (data/insights, ads, integrations, partner revenue, not-for-profit) — Describe.
- **Question (Step 2) (if Subscription or Freemium):** Pricing band and free-tier limits?
- **Options:** `free text` — e.g., "£30/month per organisation, annual 10% discount, 14-day free trial. Freemium: free tier limited to 1 yard, 5 drivers."
- **Follow-up rule:** Per-user or per-organisation pricing? Free trial length? Discount for annual? Freemium limits (how much is free?).
- **Example:** "Subscription, £30/month per yard (up to 10 drivers). Annual discount 10%. Free trial 14 days (1 yard, 5 drivers)."

### 6.3 — Monetisation Mechanics (Payments, Tax, App-Store Rules)
- **Header:** Payments
- **Mode:** text
- **Question:** How will payments work? (Stripe, PayPal, invoice, in-app purchase?) Tax/VAT implications? App-store commercial rules?
- **Options:** `free text` — Payment provider (Stripe, PayPal, direct invoice, app-store IAP), who owns billing (vendor or customer), tax/VAT jurisdiction, store commercial rules (e.g., App Store 30% cut). Reason: Varies per product.
- **Follow-up rule:** If app-store IAP: "Will you offer subscription outside the app (cheaper)?" (This avoids 30% tax and improves margins, but risks store rejection; record tension in Phase 14.)
- **Example:** "Stripe for card subscriptions. Direct invoice for annual contracts (£5k+). App Store IAP in iOS (Apple takes 30%; we price higher in-app to offset). Google Play: direct billing. VAT registered in UK (20% on UK customers only)."

### 6.4 — Tenancy Model
- **Header:** Tenancy
- **Mode:** choice
- **Question:** Is this single-tenant (one customer per deployment) or multi-tenant (many customers share infrastructure)?
- **Options:**
  - *Multi-tenant SaaS* — One database, logical isolation; scales to many customers; lowest cost; risk: data breach.
  - *Single-tenant SaaS* — One database per customer; higher cost; security / compliance advantage (e.g. HIPAA, isolated backups).
  - *Self-hosted* — Customer runs their own copy; highest cost and support; full control.
  - *Not yet decided* → Assumption; Phase 12 data/architecture explores.
- **Recommendation:** Multi-tenant SaaS (simplest, lowest cost).
- **Follow-up rule:** If multi-tenant: compliance issue (GDPR, data residency) or regulatory (HIPAA)? Single-tenant may be required.
- **Example:** "Multi-tenant SaaS. UK data residency (GDPR). Strict logical isolation per yard (database views, not row-level security for now)."

### 6.5 — White-Label or Reseller?
- **Header:** Distribution
- **Mode:** choice
- **Question:** Will this be white-labeled? Sold via resellers or partners?
- **Options:**
  - *Direct to end customers* (Recommended for v1) — Simplest v1; no reseller overhead.
  - *Reseller / partner channel* → Phase 10 adds reseller onboarding docs, partner portal.
  - *White-label* → Phase 9 adds whitelabel theme, Phase 10 adds reseller deployment guide.
  - *Not yet decided* → Deferred; Phase 15 (Launch & Adoption) revisits.
- **Example:** "Direct to small logistics yards. Reseller channel considered for v1.1 (partner with fleet-management vendors)."

---

## Phase 7 — Journeys & Functional Needs

**Rounds:** 3 rounds (+ AI sub-block: 2 rounds if enabled)



### 7.1 — Top Journeys (End-to-End)
- **Header:** Journeys
- **Mode:** text
- **Question:** List the top 3–5 end-to-end journeys. For each: trigger (what starts it?), steps (what does the user do?), outcome (what changes?).
- **Options:** `free text` — Journey name, trigger, step-by-step summary, outcome. Reason: Unique per product.
- **Follow-up rule:** For each journey: edge cases, error paths, where do users get stuck today?
- **Example:**
  - "Journey 1: Assign routes. Trigger: dispatch manager logs in at 6 AM. Steps: list today's tasks → drag drivers to routes → send to drivers. Outcome: drivers see routes in their app within 30 sec."
  - "Journey 2: Driver accepts task. Trigger: driver receives push notification. Steps: open app → read route → confirm start. Outcome: manager sees driver en route."

### 7.2 — Notifications, Reporting, Search
- **Header:** Integrations
- **Mode:** text
- **Question:** How will users be notified? (Push, email, SMS, in-app?) What reports do they need? Search / filtering? Admin tasks?
- **Options:** `free text` — Notification channels (push, email, SMS, in-app frequency), reports (daily, on-demand, export to Excel?), search scope (find drivers, zones, past routes?), admin tasks (bulk actions, role management). Reason: Varies per product.
- **Example:** "Push notifications: route assignment, driver near ETA, exception alerts. Email: daily summary. SMS: none (cost, users prefer push). Reports: daily summary (email), on-demand route history (export to CSV). Search: drivers by name/ID, zones by area. Admin: bulk import drivers, set permissions per manager."

### 7.3 — Import / Bulk Operations
- **Header:** Bulk
- **Mode:** choice
- **Question:** Does the product need to import data in bulk? (E.g., driver list, historical routes, customer zones.) Bulk update/delete actions?
- **Options:**
  - *No bulk import* → Skip. (Recommended for v1 if small data volume.)
  - *CSV import* → Phase 12 (Data, Content & Integrations) defines schema, error handling, mapping rules.
  - *API / direct database* → Phase 12 expands.
  - *Not sure yet* → Assumption; Phase 12 revisits.
- **Recommendation:** CSV import (simplest v1).
- **Follow-up rule:** If yes: volume (1000 rows? 10M?), frequency (once at launch, daily, weekly?), error tolerance (skip errors, fail entire batch, manual review)?
- **Example:** "CSV import: initial load of 500 drivers + 50 zones. Once at launch. Errors reviewed manually (email report if any row fails)."

### 7.4 — User-Generated Content & Moderation
- **Header:** UGC
- **Mode:** choice
- **Question:** Will users create content (comments, photos, notes) that needs moderation? (E.g., task notes, delivery photos, customer messages.)
- **Options:**
  - *No UGC* → Skip. (Recommended for v1.)
  - *Yes, structured* (task notes, photos, comments) → Phase 13 adds moderation rules, flagging, admin review.
  - *Yes, unstructured* (free-form messages, user profiles) → Phase 13 adds content policy, abuse reporting, auto-moderation (keyword filtering).
  - *Not sure yet* → Assumption; Phase 13 revisits.
- **Recommendation:** Structured notes only (simplest v1).
- **Example:** "Drivers add delivery notes (photo + 200-char text). No auto-moderation (low abuse risk). Manual review if flagged by manager."

### 7.5 — AI Sub-Block (Conditional: asked only if Phase 0 flagged AI as present or possible)
- **Header:** AI
- **Mode:** choice
- **Rounds:** 2 rounds (Round 1: 7.5a–c; Round 2: 7.5d–f).
- **Question:** Describe the AI/ML use case. What problem does it solve? What data does it use? What is the acceptable error rate? Human oversight needed? Cost per call? Transparency to users?

**Round 1 — Rounds: 7.5a–c**

#### 7.5a — AI Use Case & Outcome
- **Mode:** choice
- **Question:** What does the AI do?
- **Options:**
  - *Predict* — Forecast a value (e.g., route ETA, demand, failure risk).
  - *Classify* — Categorise input (e.g., delivery exception type, spam filter).
  - *Recommend* — Suggest an action (e.g., next task, route optimisation).
  - *Generate* — Create new content (e.g., route plan, transcript, summary).
- **Follow-up:** One-liner outcome (why does this matter?).
- **Example:** "Predict. Outcome: route ETA; avoid over-promising arrival times, improve customer communication."

#### 7.5b — Data & Privacy
- **Mode:** choice
- **Question:** What data does the AI use?
- **Options (multi-select):**
  - *Anonymised* — No personal identifiers; safe by design.
  - *Pseudonymised* — Identifiable via key, but keys not exposed.
  - *Personal* — Contains personal data (name, location, contact).
  - *Special-category* — Sensitive data (health, biometrics, political beliefs).
- **Data sources (free text):** Which systems/APIs provide the data? (e.g., internal logs, Google Maps, third-party API.)
- **Example:** "Anonymised. Sources: internal route history (anonymised), Google Maps live traffic (aggregated). No PII."

#### 7.5c — Acceptable Error Rate & Fallback
- **Mode:** choice
- **Question (Step 1):** How strict must the AI be?
- **Options:**
  - *Strict* — <1% error acceptable (safety-critical, financial).
  - *Moderate* — 1–5% error acceptable (business impact, user frustration).
  - *Tolerant* — >5% error acceptable (nice-to-have, low consequence).
- **Question (Step 2):** What happens if the AI fails or is uncertain?
- **Options (choose one):**
  - *Manual process* — Fall back to human decision (slower but safest).
  - *Last known value* — Use the previous known value (risky if stale).
  - *Hide feature* — Don't show the feature if AI uncertain (safest UX).
  - *Block action* — Prevent the action until AI confident (rigid).
- **Numeric tolerance (free text):** E.g., "ETA: ±10 minutes acceptable; ±30 minutes fail."
- **Example:** "Moderate tolerance. ETA ±10 min acceptable. Fallback: show last known ETA + refresh button. If >2 hours stale, hide ETA and ask user to refresh manually."

**Round 2 — 7.5d–f**

#### 7.5d — Human Oversight & Transparency
- **Mode:** choice
- **Question (Step 1):** What human oversight is needed?
- **Options:**
  - *Approves before use* — Manager/human must sign off before AI output reaches users.
  - *Can override after* — AI acts; human can override/correct after the fact.
  - *Sampled review* — Random audit of AI decisions (e.g., 10% of cases).
  - *None* — AI output is final; no human review.
- **Question (Step 2):** How transparent is the AI to users?
- **Options:**
  - *AI-generated* — Label explicitly (e.g., "AI-generated route").
  - *Estimated* — Neutral label (e.g., "ETA estimated from traffic").
  - *Not labelled* — No indication AI was involved (risky for trust).
- **Example:** "Approves before use. Manager sees 'AI-suggested route (confirm to send)'. Drivers see 'Route estimated' (no AI label)."

#### 7.5e — Cost & Rate Limits
- **Mode:** choice
- **Question:** Monthly usage ceiling?
- **Options:**
  - *<100 calls* — Very low volume (e.g., quarterly strategy).
  - *<1k calls* — Low volume (e.g., 30 calls/day).
  - *>1k calls* — High volume (e.g., 100+ calls/day).
  - *Unknown / unbounded* → Assumption; flag as [TECH-OPEN:D15] (design-interrogation estimates usage and cost).
- **Cost & volume (free text):** API cost, volume per day/month, monthly budget, rate limits.
- **Example:** "100–500 calls/day (routes + refreshes). Google Maps ETA: £0.05 per route = £750/month. Budget: acceptable within ops."

#### 7.5f — EU AI Act & Safety
- **Mode:** choice
- **Question:** If selling in EU, what is the risk class under the EU AI Act?
- **Options:**
  - *Prohibited* — Banned outright (e.g., real-time facial recognition in public). Cannot ship in EU.
  - *High-risk* — Substantial controls needed (e.g., AI used for hiring, credit decisions, critical infrastructure).
  - *Limited-minimal* — Transparency required (e.g., chatbots, logistics optimisation). Low compliance burden.
  - *Not selling in EU* — Not applicable; no EU AI Act compliance needed.
- **Escape options:** *Not sure* → Assumption; flag [TECH-OPEN:D15] (legal / design-interrogation reviews EU AI Act classification).
- **Safety controls (free text):** E.g., "Manager approval required", "Audit log of AI decisions", "User can report wrong decisions".
- **Example:** "Limited-minimal risk (logistics, not hiring/credit/critical infra). Safety: manager approval + audit log. Plan compliance checklist in Phase 13."
- **Customer mode:** This question shows EU AI Act categories for awareness; if you're not sure, mark it as [TECH-OPEN] and let design-interrogation research it.

---

## Phase 8 — UX & Wireframes

**Rounds:** 6 rounds



### 8.1 — Information Architecture (IA) & Navigation
- **Header:** IA
- **Mode:** text
- **Question:** How is the product organised? Top-level areas? Primary navigation (tabs, sidebar, hamburger, breadcrumbs)? Mental model for users (e.g., "by role", "by time", "by location")?
- **Options:** `free text` — Navigation model + diagram (text or ASCII). Reason: Unique per product.
- **ASCII preview example:**
  ```
  Web (desktop):
    [Logo] [Drivers] [Routes] [Reports] [Admin] [User Menu]
             ↓
           Drivers (list with filters)
           - Search / filter by zone, status
           - Bulk actions: assign, on leave
           - Detail: photo, phone, stats

  Mobile:
    [Dispatch] [List] [Map] [Menu]
  ```
- **Example:** "Web: left sidebar (persistent) with [Drivers] [Routes] [Reports] [Settings]. Primary interaction: drag drivers to routes (board view). Mobile: bottom tab bar [Dispatch] [List] [Map] [More]."

### 8.2 — Key Screens & States
- **Header:** Screens
- **Mode:** text
- **Question:** List the key screens. For each, the happy path + edge states (empty, loading, error, offline, no-permission).
- **Options:** `free text` — Screen names (e.g., "Route Assignment Board", "Driver Profile", "Error: Offline") with states per screen. Reason: Unique per product.
- **Follow-up rule:** For critical paths (e.g. "Assign Route"), detail error states: what if the driver is already assigned? what if sync fails?
- **Example:**
  - "Route Assignment Board: empty (no routes), loading (spinner), success (board with cards), error (retry banner), offline (show last-cached state + 'changes saved when online')."
  - "Driver Profile: success (all fields), loading, no-permission (show 'Contact manager'), error (retry)."

### 8.3 — Onboarding & First-Run Experience
- **Header:** Onboarding
- **Mode:** choice
- **Question:** How should new users get started? (How intrusive vs. helpful?)
- **Options:**
  - *Minimal* (contextual help only) → Tooltips on first use; progressive disclosure; no forced tour. Best for power users or simple products.
  - *Light intro* (2–3 min) → Quick skippable tour of key features; guided walkthrough optional.
  - *Hands-on tutorial* (5–10 min) → Sample data; users complete their first real task step-by-step.
  - *Full support package* → Tutorial + in-app help link + email support (for enterprise).
- **Recommendation:** Light intro (balances helping new users without frustrating power users).
- **Follow-up rule:** Who writes copy? (Phase 8 content ownership.) Supported languages?
- **Example:** "Light 3-min tour (skippable). First time at the route board: highlight 'drag driver to route'. In-app help link → knowledge base. Tutorial video (5 min) in help centre for new customers."

### 8.4 — Content & Tone of Voice
- **Header:** Content
- **Mode:** text
- **Question:** Who writes UI copy (labels, buttons, error messages, help text)? What tone? (Formal, friendly, technical?) Plain-English target or jargon OK?
- **Options:** `free text` — Copy owner (PM, design team, writing team), tone (formal / friendly / technical), plain-language target, examples of tone you like. Reason: Varies per product.
- **Example:** "Tone: professional, no jargon (dispatch managers know logistics but not tech). Copy owner: PM + Designer (I write, design team reviews). Example tone: Slack (clear, friendly, no corporate jargon)."

### 8.5 — Forms & Validation Behaviour
- **Header:** Forms
- **Mode:** choice
- **Question:** How should forms behave? (Real-time validation with inline error, validate-on-submit, disable submit until all fields valid?)
- **Options:**
  - *Real-time validation (inline, as-you-type)* — Shows errors immediately; user can fix mid-typing. (Recommended for web.)
  - *Validate-on-blur* — Shows error when user leaves a field; balances speed and guidance.
  - *Validate-on-submit* — Show all errors at once; simplest, but less helpful.
  - *Progressive forms* — One question per screen (Recommended for mobile).
- **Recommendation:** Real-time on web, validate-on-blur on mobile.
- **Example:** "Create Driver form: real-time validation. Name required (check on blur). Email validated with regex + verify-email (optional, v1.1). Phone: optional. Submit disabled until name + one contact filled."

### 8.6 — Feedback, Undo & Reassurance
- **Header:** Feedback
- **Mode:** choice
- **Question (Step 1):** How should the app confirm actions?
- **Options:**
  - *Toast/snackbar (non-intrusive)* — Brief notification (top/bottom, 3 sec auto-dismiss); user can continue; low cognitive load.
  - *Inline success* — Text/icon appears next to the button; brief confirmation; good for forms.
  - *Modal confirmation* — Modal dialog requiring acknowledgement; for high-stakes actions (delete, unassign).
- **Question (Step 2):** Undo available? For how long?
- **Options:**
  - *No undo* — Actions are final; higher burden on the user (need confirmation dialogs).
  - *Undo (5 min)* — Brief undo window; manageable for most; balance UX and data consistency.
  - *Undo (full session)* — Undo available until logout; maximum safety; higher complexity.
- **Question (Step 3):** Destructive actions (delete, reassign, mass-change) need explicit confirmation?
- **Options:**
  - *Confirmation modal for all* → Safety; slower workflows.
  - *Confirmation for batch/mass only* → Balance; single actions are quick, batch actions safer.
  - *Confirmation for high-impact only* → Examples: delete account, reassign all drivers to different manager. Fast UI for routine actions.
- **Example:** "Assign route: inline success (checkmark + 'Assigned'). Unassign: confirmation modal. Undo: 5-min window for reassign/unassign (flagged 'Changed by Manager' in driver app). Destructive: confirm for batch-unassign (>5 drivers), not for single-route changes."
- **Mapping:** Constrains Phase 9 (UI feedback components, modal styling, toast position), Phase 8 content & tone (wording of confirmations).

### 8.7 — Notifications & E-mail Design
- **Header:** Alerts
- **Mode:** text
- **Question:** What events trigger notifications? (Driver assigned, exception, reminder.) Push + email design: frequency (real-time, batched, daily digest), do-not-disturb hours?
- **Options:** `free text` — Event triggers, channels (push, email, SMS, in-app), frequency, quiet hours, sample copy. Reason: Varies per product.
- **Example:** "Driver assigned: immediate push (1 title + body). Exception (late ETA): immediate push + SMS. End-of-day summary: email (6 PM, digest of all exceptions + completions). No notifications 10 PM–6 AM."

### 8.8 — Accessibility Target & Localisation
- **Header:** A11y
- **Mode:** text
- **Question:** Accessibility target: WCAG AA (default), AAA, or A? Localisation scope: languages to launch, RTL support, text-expansion room (German 30% longer)?
- **Options:** `free text` — WCAG level (default AA), languages for v1 (others v1.1+), RTL, text-expansion %. Reason: Constrained by Phase 2 audience.
- **Example:** "WCAG AA (non-negotiable per audience research). English + Dutch for v1. No RTL. German text ~15% expansion room (left in English copy). Font scaling supported: 100–200% with reflow."

### 8.9 — Responsive Behaviour & Devices
- **Header:** Responsive
- **Mode:** text
- **Question:** For each device (phone, tablet, desktop, desktop + multiple windows), how does layout adapt? (Stack vertically, hide columns, drawer, split-view?)
- **Options:** `free text` — Breakpoints (phone <600px, tablet 600–900px, desktop >900px) and layout per breakpoint. Reason: Constrained by Phase 2/10 devices.
- **ASCII preview example:**
  ```
  Mobile (< 600px):       Tablet (600–900px):         Desktop (> 900px):
  [Header]                [Sidebar] [Content]         [Sidebar] [Content]
  [Nav tabs]              Full width, sidebar         Persistent, full width
  [Content full-width]    collapsible                 Drag to resize
  ```
- **Example:** "Phone: bottom tabs, full-width content, sidebar slides in as drawer. Tablet: left sidebar (collapsible), main area flexes. Desktop: persistent sidebar, drag resize."

### 8.10 — Prototype Show-Back (Wireframe Reaction)
- **Header:** Wire OK
- **Mode:** choice
- **Question:** (Presented as wireframes are shown, not asked in advance.) React to the wireframes. Do you accept this navigation and content structure?
- **Reaction options (fixed set):**
  - *Accept* → Wireframes approved; move to Phase 9 (UI design).
  - *Change* (free text: what to change) → Note the change, revise wireframe, re-show.
  - *Reject* → Major rethink needed. Record as PD-decision (Rejected).
  - *Question* → Flag unclear area; skip for now (Phase 9 show-back may resolve).
- **Mapping:** Each reaction logged as PD-decision: Accept → Resolved; Change → Resolved + new PD; Reject → Conflict or Resolved; Question → Deferred.

**Playback Checkpoint:** *"To summarise Phase 8: you want {summary of IA, top screens, onboarding, tone, notifications, accessibility}. Correct, or should we adjust anything?"*

---

## Phase 9 — UI & Visual Design + Mockups

**Rounds:** 5 rounds



### 9.1 — Brand & Existing Design System
- **Header:** Brand
- **Mode:** text
- **Question:** Do you have an existing brand, design system, or Figma file? (Logo, colour palette, typography, component library.)
- **Options:** `free text` — Figma link, design-system URL, logo asset, brand guidelines doc. Reason: Varies per product.
- **Example:** "Brand guidelines doc (internal). Logo: SVG. Figma: https://figma.com/file/xyz (shared view). Design system: UI Kit in Figma (Fluent UI components)."

### 9.2 — Accent Colour & Theme Generation
- **Header:** Colour
- **Mode:** text
- **Question:** What is the primary accent colour (hex or HSL)? This drives all theme tokens (light, dark, high-contrast).
- **Options:** `free text` — Hex (e.g., #0078D4) or HSL (hsl(205, 100%, 42%)). Reason: Unique per product.
- **ASCII preview (optional):**
  ```
  Colour input: #0078D4 (Microsoft Blue)
                ↓
  css-theme-generator
                ↓
  Token pairs generated:
    Light theme: bg=white, text=dark, accent=#0078D4, hover=#106ebe
    Dark theme: bg=#1e1e1e, text=light, accent=#0078D4, hover=#1084ff
    High-contrast: bg=black, text=white, accent=#0078D4 (high sat)
  ```
- **Mapping:** Tokens feed mockups, prototype, and later the product build.
- **Example:** "Accent: #0078D4 (brand blue, approved 2026-10-15). Prefer to follow Fluent UI standard tokens for consistency."
- **Customer mode rewrite:** What is the main brand colour you want to use? (We'll use this to generate the light and dark themes automatically.)

### 9.3 — Typography (Font Family, Weights, Sizes)
- **Header:** Typography
- **Mode:** text
- **Question:** Font family (serif, sans-serif, system, custom)? Sizes and weights for headings, body, small text?
- **Options:** `free text` — Font (e.g., "Segoe UI, fallback to system sans"), sizes (h1 32px, h2 24px, body 14px, small 12px), weights (bold for headings, regular body). Reason: Varies per product.
- **Example:** "Font: Segoe UI (Windows standard, available on macOS via system, fallback to -apple-system). Sizes: H1 32px/700, H2 24px/700, body 16px/400, small 12px/400. Line-height 1.5 body, 1.2 headings."

### 9.4 — Themes (Light, Dark, High-Contrast)
- **Header:** Themes
- **Mode:** choice
- **Question:** Which themes should be available? Light (default), dark, high-contrast (for accessibility)?
- **Options:**
  - *Light only* → Simplest; Phase 2 audience accepts light mode. (Recommended for v1.)
  - *Light + dark* → Default light; users can toggle. (Recommended if outdoor use or evening shifts.)
  - *Light + dark + high-contrast* → Accessibility requirement (Phase 2 accessibility findings).
  - *System preference (auto-switch)* → Respects OS setting; Phase 10 tech complexity noted.
- **Recommendation:** Light + dark (modern expectation; low cost).
- **Follow-up rule:** If high-contrast: contrast ratios must be checked against WCAG level (Phase 8 accessibility) before mockups shown.
- **Example:** "Light (default) + dark (users can toggle in settings). High-contrast deferred to v1.1 (small accessibility need, add if time permits)."

### 9.5 — Density & Component Library
- **Header:** Density
- **Mode:** choice
- **Question:** How dense should the UI be? (Comfortable = 16px spacing, compact = 8px, dense = 4px.) Which component library (Fluent UI for Blazor, MAUI for mobile, etc.)?
- **Options:**
  - *Comfortable* — Generous spacing, large targets; good for mobile, newer users. (Recommended for v1.)
  - *Compact* — Standard Fluent/Material spacing; balance.
  - *Dense* — Minimal spacing; power users, data-heavy views. (Recommended for internal/admin tools.)
- **Library (Awareness only; [TECH-OPEN:D9] — do not record as a decision; design-interrogation decides):**
  - Web: Fluent UI, Material UI, or custom.
  - iOS: MAUI or SwiftUI.
  - Android: MAUI or native Material Design.
  - Desktop: WinUI (Windows), AppKit (macOS).
- **Recommendation:** Comfortable density + Fluent UI (template standard).
- **Mapping:** Informs Phase 10 (component library choice) and Phase 9 mockups (CSS class generation).
- **Example:** "Comfortable density (dispatch managers may be older, outdoor use). Fluent UI for web, MAUI native components for iOS/Android, WinUI for Windows."
- **Customer mode rewrite:** How much whitespace should there be? Do you want the UI packed with features (dense), or spread out for easier reading (comfortable)?

### 9.6 — Iconography, Imagery & Illustration Style
- **Header:** Visuals
- **Mode:** choice
- **Question (Step 1):** What icon style fits your brand?
- **Options:**
  - *Fluent UI icons* → Microsoft's Fluent Design; professional, clean; matches Blazor web apps; consistent.
  - *System icons (platform native)* → iOS SF Symbols, Material Design icons; platform idiomatic; cost-effective.
  - *Custom icons* → Bespoke look; higher cost; ensures uniqueness.
  - *Emoji or emoji-style* → Playful, modern; risky if audience finds it unprofessional.
- **Question (Step 2):** Photos and illustrations — how realistic should they be?
- **Options:**
  - *Realistic photos* — Professional photography of real people, products, places; trustworthy; high cost. Rule: no identifiable real people; image licence checked and recorded.
  - *Lifestyle/illustrated* — Curated photos + icons; cleaner than pure photography; mid-cost.
  - *Abstract / minimal* → Minimal, geometric; premium feel; abstract shapes, no real people.
  - *None* → Icons and typography only; simplest; good for B2B, technical products.
- **Example:** "Icons: Fluent UI (consistent with Blazor). Photos: realistic logistics scenes (vehicles, yards, outdoor work), no identifiable people, licence checked. Illustrations: none for v1. No emoji (too casual for logistics)."
- **Mapping:** Constrains Phase 9 mockups (which assets are used); Phase 10 deliverables (design-system token package).

### 9.7 — Motion, Animation & Haptics
- **Header:** Motion
- **Mode:** choice
- **Question:** Should the UI animate or should it be static? (Transitions, loading spinners, success animations, micro-interactions.) Haptic feedback on mobile?
- **Options:**
  - *Static (no animation)* → Fastest performance; safest for accessibility. (Recommended for field work / low-connectivity.)
  - *Subtle motion* (transitions 200ms, focus, hover) → Better UX without distraction.
  - *Moderate motion* (success animations, loading patterns, page transitions) → Engaging but not distracting. (Recommended for web.)
  - *Rich motion* (elaborate transitions, parallax, micro-interactions) → Highest engagement; risk of distraction / motion-sickness.
- **Haptics:** (Mobile only)
  - *None* → Simplest; Phase 2 audience accepts.
  - *Light haptics* (tap, success, error) → (Recommended for mobile.)
  - *Rich haptics* (multiple patterns per action) → V2.
- **Recommendation:** Subtle motion on web, light haptics on mobile.
- **Follow-up rule:** If motion, check Phase 8 accessibility (reduced-motion flag; disable animations for users who set it).
- **Example:** "Subtle motion: 200ms transitions between screens, focus ring visible on keyboard nav, success toast fades in/out. Haptics: light tap on button press, success buzz when route assigned. Respect prefers-reduced-motion media query."

### 9.8 — Design Deliverables & Approvals
- **Header:** Deliverables
- **Mode:** text
- **Question:** What design files/documents do you need? (Figma, design specs, component guide, accessibility checklist, design-to-dev handoff document?)
- **Options:** `free text` — Deliverable list (e.g., "Figma design system, design specs, dev handoff doc, accessibility audit report"). Reason: Varies per product.
- **Example:** "Figma (main source of truth). Design specs (margin, padding, colour tokens, font sizes) exported to JSON for dev. Accessibility audit (contrast, focus order, screen-reader labelling) in Phase 9. Design-to-dev handoff via Figma comments + component mapping."

### 9.9 — Mockup Show-Back (Reaction & Revision)
- **Header:** Mockup OK
- **Mode:** choice
- **Question:** (Presented as mockups are shown, not asked in advance.) React to the mockups. Do you accept this look & feel?
- **Reaction options (fixed set):**
  - *Accept* → Mockups approved; move to Phase 10 (Platforms & Deliverables).
  - *Change* (free text: what to change, e.g. "darker blue", "larger text", "remove animation") → Note the change, revise mockup, re-show.
  - *Reject* → Major redesign needed. Record as PD-decision (Rejected).
  - *Question* → Unclear aspect (e.g., "does this work on iPad?"). Noted; Phase 10 / Phase 11 show-back may resolve.
- **Mapping:** Each reaction logged as PD-decision: Accept → Resolved; Change → Resolved + new PD; Reject → Conflict or Resolved; Question → Deferred.

**Playback Checkpoint:** *"To summarise Phase 9: you want {summary of brand, accent colour, font, density, icons, motion, accessibility features}. Correct, or adjustments needed?"*

---

## Phase 10 — Platforms & Deliverables

**Rounds:** 4 rounds



### 10.1 — Web [TECH-OPEN]
- **Header:** Web
- **Mode:** choice
- **Question (Step 1):** Build for web? If yes: what kind of web experience?
- **Options:**
  - *No web* → Skip to 10.2.
  - *Public site* → Informational landing page; static/marketing content; SEO-driven.
  - *Authenticated app* → Login required; SaaS or internal tool; user data.
  - *Public site + authenticated app* → Landing page + app behind login; freemium or tiered access.
- **Question (Step 2) (if not "No web"):** Rendering model (technical, flagged TECH-OPEN for decision in design-interrogation):
- **Options (for respondent awareness only; [TECH-OPEN:D9] — do not record as a decision; design-interrogation will finalize):**
  - *Blazor Server* → Server-side rendering; always online; best for interactive, realtime apps.
  - *Blazor WASM* → Client-side; offline capable; works from file system.
  - *Blazor Auto* → Hybrid; server initially, then WASM on client.
  - *Custom SPA (React/Vue/Angular) + backend API* → Separate frontend/backend; maximum flexibility.
- **Question (Step 3):** Other web choices:
- **Options (multi-select from):**
  - *PWA (installable)* → Add-to-home-screen capability; web app on app stores.
  - *SEO-friendly* → OpenGraph, meta tags, structured data; needed for public-facing products.
  - *Offline-capable* → Service workers, local storage, sync-on-reconnect.
- **Browser/OS support:** Modern browsers (Chrome/Firefox/Safari latest 2 versions) standard; older support requires design-interrogation assessment.
- **Performance budget:** (Optional) e.g., "FCP <2s on 4G, page <1MB".
- **Follow-up rule:** Browser support and SEO needs are technical; pass to design-interrogation Dimension 9 (Client Surfaces & UX Architecture). Performance budget: frames the trade-off between feature richness and speed.
- **Example:** "Web app (authenticated, internal tool). PWA preferred (add to home). Chrome/Firefox/Safari latest (no IE11 support needed). FCP <2s target. Rendering model (Blazor Auto vs. WASM): to be decided in design-interrogation."
- **Customer mode:** This question is technical (rendering model); we ask it to show what choices exist, but design-interrogation makes the final call. You can answer Step 1 (web needed?) and Step 3 (PWA, offline?); skip Step 2 and the browser-support discussion if they feel too deep.

### 10.2 — Mobile (iOS & Android) [TECH-OPEN]
- **Header:** Mobile
- **Mode:** choice
- **Question (Step 1):** Build for mobile?
- **Options:**
  - *No mobile* → Skip to 10.3.
  - *iOS only* → iPhone/iPad only; high-end users.
  - *Android only* → Android phones/tablets; cost-conscious or emerging markets.
  - *iOS + Android* → Both platforms; majority of users.
- **Question (Step 2) (if mobile selected):** Form factor and offline needs:
- **Options:**
  - *Phone only, online-required* → Simplest; internet always available.
  - *Phone + tablet, mostly online* → Responsive layouts; occasional offline OK.
  - *Phone + tablet, offline-first* → Local sync, conflict resolution; field work needs.
  - *Tablet primary* → Desktop-like experience on tablet; less common.
- **Question (Step 3):** Which device features do you need? (Multi-select; spread over 2 rounds: 4+4+2 options.)
  - *Round 3a (4 options):* GPS location, Camera photos, Biometric auth, Push notifications.
  - *Round 3b (4+2 options):* NFC, Bluetooth, Contacts, File access, Health data, Payment.
- **Question (Step 4):** Framework (technical, flagged TECH-OPEN):
- **Options (for respondent awareness only; [TECH-OPEN:D9] — do not record as a decision; design-interrogation will finalize):**
  - *MAUI (C# native)* → .NET stack; iOS, Android, Windows, macOS; cross-platform code.
  - *Blazor Hybrid* → Blazor components in native shells; blend web + native.
  - *Responsive web (PWA)* → One codebase for all; simplest but less native feel.
  - *Native per platform* → Separate iOS/Android; maximum polish; highest cost.
- **OS support:** iOS 14+ and Android 11+ standard; older versions require design-interrogation assessment.
- **Follow-up rule:** Device features (GPS, camera, biometrics) drive identity/permissions/privacy in design-interrogation. Framework is technical.
- **Example:** "iOS + Android, phone + tablet, offline-first (field drivers work underground). MAUI shared UI. Device features: GPS required, camera optional, push required. iOS 14+, Android 11+."
- **Customer mode:** Platforms and device features you can answer (Steps 1–3); framework choice (Step 4) is technical and deferred to design-interrogation.

### 10.3 — Desktop (Windows, macOS) [TECH-OPEN]
- **Header:** Desktop
- **Mode:** choice
- **Question (Step 1):** Build for desktop?
- **Options:**
  - *No desktop* → Skip to 10.4.
  - *Windows only* → Windows 10+.
  - *macOS only* → macOS 11+.
  - *Windows + macOS* → Both platforms; internal tools often cover both.
- **Question (Step 2a) (if Windows selected):** Windows installer type (technical, flagged TECH-OPEN):
- **Options (for respondent awareness only):**
  - *MSIX* → Modern, auto-update, Microsoft Store or web distribution.
  - *MSI* → Traditional; manual updates; older OS support.
  - *Portable* → No installer; simplest; no auto-update.
  - *Store* → Microsoft Store distribution; automatic updates.
- **Question (Step 2b) (if macOS selected):** macOS installer type (technical):
- **Options:** *DMG (standard drag-to-applications)* / *Mac App Store* / *Portable*.
- **OS integration (multi-select):** File associations (open .xyz files in this app), shell/context-menu integration, tray icon (Windows) / menu bar (macOS), printing.
- **OS support:** Windows 10+, macOS 11+ (latest 2 versions standard).
- **Framework (technical, flagged TECH-OPEN):**
- **Options (for respondent awareness only; [TECH-OPEN:D9] — do not record as a decision; design-interrogation will finalize):**
  - *MAUI* → Shared C# UI; iOS, Android, Windows, macOS.
  - *WPF* → Windows only; rich desktop; mature framework.
  - *MAUI Mac Catalyst* → macOS native via MAUI.
  - *Separate native per platform* → Maximum polish; highest cost.
- **Follow-up rule:** Installer and code-signing are technical; design-interrogation decides. Auto-update strategy (store vs. web) affects delivery. File associations and OS integration add complexity.
- **Example:** "Windows + macOS (internal tool; HQ Macs, yards Windows). Framework: MAUI shared. Installer: MSIX (Windows, auto-update). DMG (macOS, unsigned v1). Tray icon (Windows), menu bar (macOS). No shell integration (v2)."
- **Customer mode:** You can answer Step 1 (desktop needed?) and OS integration choices; Steps 2a/b/Framework are technical and deferred to design-interrogation.

### 10.4 — Cross-Surface & Feature Parity
- **Header:** Parity
- **Mode:** text
- **Question:** What must be identical across web, iOS, Android, Windows, macOS? What is platform-idiomatic (different)?
- **Options:** `free text` — Feature parity table (feature / web / iOS / Android / desktop, mark identical or per-platform). Reason: Varies per product.
- **Example:**
  ```
  Feature       | Web    | iOS    | Android | Windows | macOS
  Route assign  | ✓ same | ✓ same | ✓ same  | ✓ same  | ✓ same
  Drag-drop     | ✓ yes  | n/a    | n/a     | ✓ yes   | ✓ yes
  Real-time map | ✓ yes  | ✓ yes  | ✓ yes   | ✓ yes   | ✓ yes
  Desktop notif | n/a    | ✓ iOS  | ✓ FCM   | ✓ Win   | ✓ macOS
  ```
- **Mapping:** Informs Phase 12 (backend architecture, API design, state sync).

### 10.5 — Data Backend & API
- **Header:** Backend
- **Mode:** choice
- **Question:** One backend serving all surfaces, or per-surface BFF (Backend-for-Frontend)? [TECH-OPEN]
- **Options:**
  - *One backend API* → REST / GraphQL / gRPC, all surfaces consume same.
  - *Per-surface BFF* → Web BFF, Mobile BFF, Desktop BFF (each tailored to its platform).
  - *Not yet decided* → Assumption; design-interrogation will decide.
- **Recommendation:** One backend API (simpler for v1).
- **Mapping:** Phase 12 (API design, scaling, multi-tenancy).

### 10.6 — Other Deliverables
- **Header:** Other
- **Mode:** choice
- **Question (Step 1):** Which deliverable categories apply? (Multi-select up to 4; *Other* for custom.)
- **Options:**
  - *Developer-facing* (API, SDK, documentation) → If third-party integrations or client libraries needed.
  - *Internal operations* (Admin portal, back-office, support runbooks, demo/sandbox) → If internal team management, reporting, troubleshooting needed.
  - *Customer-facing* (Marketing site, training materials, accessibility statement) → If public-facing or onboarding needed.
  - *Other* → Custom deliverables.
- **Question (Step 2) (for each category selected):** Which specific items in that category?
- **Developer-facing options:**
  - *Public API (REST/GraphQL)* → Third parties integrate.
  - *SDK / Kiota client* → Developers use API easily.
  - *API documentation* → OpenAPI spec, error codes, examples.
- **Internal options:**
  - *Admin portal* → User management, reporting, compliance.
  - *Support runbooks* → Incident response, troubleshooting.
  - *Demo/sandbox environment* → Test data, training.
- **Customer-facing options:**
  - *Marketing website* → Landing page, pricing, sign-up.
  - *Training videos/guides* → Onboarding, feature tutorials.
  - *Accessibility statement* → Public commitment + known issues.
  - *Help centre / knowledge base* → FAQ, user guides.
- **Follow-up rule:** For each deliverable selected: owner, v1 vs. v1.1+, acceptance criterion.
- **Example:** "Developer-facing: API + Kiota SDK (v1.1). Internal: Admin portal (v1, PM manages). Customer-facing: Marketing site (v1), help centre (v1.1). Accessibility statement (v1, compliance)."

**Deliverables Register (output as `DLV-nnn` in platform-deliverables.md):**

| DLV ID | Deliverable | Platforms | Owner | Acceptance Criterion | Release Phase |
|---|---|---|---|---|---|
| DLV-001 | Web app (Blazor Auto, authenticated) | Web | Dev team | Route assignment works, real-time sync, WCAG AA, FCP <2s | v1.0 |
| DLV-002 | iOS app (MAUI) | iOS phone + tablet | Dev team | Runs on iOS 16+, offline-first, camera optional | v1.0 |
| DLV-003 | Android app (MAUI) | Android phone + tablet | Dev team | Runs on Android 11+, offline-first, GPS | v1.0 |
| DLV-004 | Windows desktop (MSIX) | Windows 10+ | Dev team | Installer, auto-update, tray icon | v1.1 |
| DLV-005 | macOS desktop (DMG) | macOS 11+ | Dev team | Installer (unsigned v1), menu bar icon | v1.1 |
| DLV-006 | Admin portal | Web | PM + backend | User CRUD, reporting, role management | v1.0 |
| DLV-007 | API documentation | Web | Backend engineer | OpenAPI spec, quick-start, error codes | v1.0 |
| DLV-008 | Accessibility statement | Web | Compliance | Published on website, known issues listed | v1.0 |

---

## Phase 11 — Mocks & Clickable Prototype

**Rounds:** 2 rounds (walkthrough + final reaction)



(Mechanics: wireframes are shown at the end of Phase 8; mockups at the end of Phase 9; clickable prototype assembled in Phase 11 from approved designs. This phase wraps up the visual outputs and runs a scripted walkthrough + validation.)

### 11.1 — Walkthrough & Validation Script
- **Header:** Validation
- **Mode:** choice
- **Question (Readiness):** Before we walk through the prototype, how do you want to interact?
- **Options:**
  - *Own device* — You'll interact with the prototype on your own screen/keyboard/mouse.
  - *Screen-share* — You'll watch and direct while I drive the prototype.
  - *Facilitator drives* — I'll walk through key tasks and ask for observations.
- **Purpose:** Task-based validation: respondent attempts or observes 5–8 key journey tasks (e.g., "assign a route", "confirm delivery", "view daily report") and reports success/struggle/failure. Each task outcome recorded with observation, resulting change to the prototype / design.
- **Task rendering (one question per task; reaction options fixed):**
  - Task: [Description of the scenario and objective]
  - Reaction options: *Succeeded* (task completed as expected) / *Struggled* (completed with difficulty) / *Failed* (could not complete) / *Other* (free text).
  - Observation: [What worked, what confused, where stuck?] (free text; required if Struggled or Failed).
- **Script example:**
  ```
  Task 1: "Assign Alice (driver) to the 10 AM route."
    Reaction: Struggled
    Observation: "Found the 'Assign' button but didn't expect the confirmation dialog. Had to look twice."
    Change: [PD-decision if needed]
  ```

### 11.2 — Prototype Review Reactions
- **Header:** Proto OK
- **Mode:** choice
- **Question:** Having walked through the prototype, does it represent what you want to build?
- **Reaction options (fixed set):**
  - *Accept* → Prototype approved; sign-off ready.
  - *Change* (free text: what to change) → Note the change, revise, re-show sub-set.
  - *Reject* → Major rethink. Record as PD-decision (Rejected).
  - *Question* → Unclear aspect. Noted for Phase 17 (Completeness check).
- **Mapping:** Recorded as final PD-decision (Prototype sign-off): Accept → Resolved; Change → Resolved + new PD; Reject → Conflict or Resolved; Question → Deferred.

---

## Phase 12 — Data, Content & Integrations (Business View)

**Rounds:** 3 rounds



### 12.1 — Data Ownership & Migration
- **Header:** Data
- **Mode:** text
- **Question:** What data does the product own? What is imported from third parties? Data migration from legacy systems?
- **Options:** `free text` — Data types (drivers, routes, zones, photos, history, audit logs), ownership (product owns vs. imports from X), migration plan (one-time at launch, ongoing sync, legacy data ETL). Reason: Varies per product.
- **Follow-up rule:** For migrated data: volume, format (CSV, database dump, API), validation needed before go-live.
- **Example:** "Product owns: drivers, routes, tasks, delivery photos, timestamps. Imports from: customer systems (driver list, zone definitions via CSV). Migrates from: legacy dispatch log (500k rows of route history, data cleansing required)."

### 12.2 — Third-Party Services & Integrations
- **Header:** Integrations
- **Mode:** choice
- **Question (Step 1):** Which integration categories do you need? (Multi-select from 4 per round; two rounds.)
- **Round 1 (4 options):**
  - *Payments* — Stripe, PayPal, Square, others. (Phase 6 pricing determines.)
  - *Identity / SSO* — Auth0, Microsoft, Apple Sign-in, LDAP. (Phase 14.)
  - *Maps & routing* — Google Maps, MapBox, TomTom. (Phase 7 journeys; Phase 10 GPS.)
  - *Email / SMS / Push* — SendGrid, Twilio, Firebase. (Phase 7 notifications.)
- **Round 2 (4 options):**
  - *Analytics* — Google Analytics, Mixpanel, Amplitude, custom event tracking. (Phase 4 tracking plan.)
  - *ERP / CRM* — Salesforce, SAP, NetSuite, custom API. (Phase 6 business model.)
  - *Reporting* — Power BI, Tableau, custom dashboards. (Phase 4 KPIs.)
  - *Other* — Custom integrations (free text).
- **Question (Step 2):** For each category selected, which vendor(s)?
- **Options:** `free text` — Vendor names + rationale (cost, features, existing relationships).
- **Recommendation:** Choose incumbent vendors for each category; avoid "build it ourselves" for commodity services.
- **Follow-up rule:** For each integration: cost, API rate limits, data residency, fallback if down.
- **Example:** "Payments: Stripe (cards + PayPal). Identity: Microsoft (Azure AD for B2B), Apple Sign-in optional (v1.1). Maps: Google Maps (routing, ETA). E-mail: SendGrid. Analytics: custom events (Mixpanel, deferred). No ERP sync for v1."

### 12.3 — Content Ownership & Localisation
- **Header:** Content
- **Mode:** text
- **Question:** Who writes and approves product copy (labels, help text, onboarding)? Help centre / knowledge base? Legal text (T&Cs, privacy policy) ownership?
- **Options:** `free text` — Copy owner (PM, writer, vendor), approval process, help-centre platform (Zendesk, Intercom, self-hosted), legal-text owner (legal team, vendor). Reason: Varies per product.
- **Example:** "Copy owner: PM (I write, design + product team reviews). Help centre: self-hosted markdown site on GitHub Pages (no Zendesk cost). Legal text: external counsel (I coordinate; they approve T&Cs, privacy, cookies)."

---

## Phase 13 — Compliance, Legal & Risk

**Rounds:** 4 rounds



### 13.1 — GDPR & Data Protection
- **Header:** GDPR
- **Mode:** choice
- **Question (Conditional: asked if Phase 2 or Phase 3 indicates EU customers or sensitive data):** GDPR applies. What's your consent model for data collection?
- **Options:**
  - *Opt-in explicit consent* → User must actively agree to data collection (location, cookies, etc.); safest; users may decline.
  - *Legitimate interest* → Collect data needed for service (email, name); document the business case; users can opt out.
  - *Opt-out with notice* → Collect by default; user can disable; works if service needs the data.
  - *Not sure / will research* → Assumption; legal team decides in Phase 13.
- **Follow-up rule:** Which PII types are collected? (Name, email, phone, location, IP, photos, cookies, device IDs.) For each: retention period, deletion on request, who can access. Phase 2 answers (2.7 accessibility, 2.10 minors) are captured as facts; Phase 13 only confirms legal specifics.
- **Multi-select:** Data residency options (EU data centres only, UK or EU, US + EU, other).
- **Example:** "EU customers. Consent: opt-in for location tracking (needed for GPS), legitimate interest for email/name. Data residency: EU. PII: driver name, phone, location. Location retained 90 days then aggregated. Deletion on request within 30 days. DPA with Google Maps, Stripe. DPIA needed (location, driver profiling)."
- **Mapping:** Constrains Phase 13 legal review, Phase 14 technical architecture (data storage, encryption).
- **Customer mode rewrite:** If you operate in the EU: do you ask users for permission before collecting their data (like location, photos), or is it needed for the service to work?

### 13.2 — Industry Regulations & Compliance Standards
- **Header:** Regulations
- **Mode:** choice
- **Question:** Industry-specific compliance rules? (Multi-select up to 4; *None* if not applicable.)
- **Options (most common):**
  - *HIPAA* (healthcare) → PHI protection, audit logs, encryption, vendor agreements.
  - *PCI-DSS* (payment card data) → Usually delegated to Stripe/PayPal; we don't store card details.
  - *SOC 2 Type II* (B2B SaaS) → Operational controls, security, availability, confidentiality audit.
  - *ISO 27001* (information security) → Formal security management; high-assurance products.
- **Escape options:** *None / Not applicable* → Typical B2C/B2B products (logistics, e-commerce) don't require industry-specific rules beyond GDPR/accessibility.
- **Follow-up rule:** If any standard selected: when is certification needed (v1 or later)? Who is responsible?
- **Example:** "Logistics app: no HIPAA, no PCI-DSS (use Stripe). No SOC 2 for v1 (may add v1.1 if Enterprise customers demand). Accessibility law applies (EN 301 549 if EU customers). Privacy policy required (Phase 13)."
- **Mapping:** Drives compliance roadmap, security controls, audit schedule.

### 13.3 — Accessibility Law & Legal Obligation
- **Header:** A11y law
- **Mode:** text
- **Question:** (If Phase 2 flagged accessibility need or EU/UK customers:) WCAG level required by law? (WCAG AA = industry default; AAA = stricter; EN 301 549 = EU public sector / critical digital; EAA = EU accessibility act.)
- **Options:** `free text` — Legal requirement (jurisdiction, standard, deadline), internal target (WCAG AA / AAA), exemptions known. Reason: Constrained by jurisdiction.
- **Example:** "UK customers; no legal accessibility mandate for private sector logistics app. Internal target: WCAG AA (good practice, improves usability). Phase 8/9 check colours, focus, keyboard nav against AA."

### 13.4 — Minors & Vulnerable Data
- **Header:** Minors
- **Mode:** choice
- **Question:** Does the product handle minors' data or involve vulnerable people? Parental consent, child-safety rules, content policy?
- **Options:**
  - *No minors, no vulnerable people* — Standard case; no special protections required.
  - *Minors use it (under 16, under 13)* → Parental consent, data minimisation, content moderation.
  - *Vulnerable people (elderly, disabled, asylum seekers, patients)* → Duty of care, safeguarding rules, simplified design.
- **Example:** "Drivers are 18+ (employment requirement). No minors. Not vulnerable-person app (logistics staff)."

### 13.5 — Licensing & Open-Source Obligations
- **Header:** Open-source
- **Mode:** text
- **Question:** Open-source libraries used? License obligations (MIT, GPL, Apache 2.0 compliance)? Must we publish our code?
- **Options:** `free text` — License scan (SBOM), copyleft concerns (GPL requires source release; MIT does not), proprietary code status. Reason: Varies per tech stack.
- **Follow-up rule:** If GPL detected: can we distribute under GPL, or must we relicense? Risk assessment.
- **Example:** "Fluent UI (MIT), MAUI (MIT), SendGrid SDK (MIT). No GPL. No copyleft concerns. Product code is proprietary (no open-source requirement)."
- **[TECH-OPEN:D9] skip in Customer mode** — licence scan is a technical decision; design-interrogation handles it.

### 13.6 — Terms, Privacy Policy, Cookie Consent
- **Header:** Legal docs
- **Mode:** text
- **Question:** Terms of service, privacy policy, cookie banner, data-processing agreement. Who writes / approves? Template or custom?
- **Options:** `free text` — Ownership (legal team, vendor, template), publication (website, in-app, email), update process. Reason: Varies per product.
- **Example:** "Legal team drafts T&Cs + privacy (based on company template). PM approves. Published on website + in-app (onboarding). Cookie consent: implicit (we don't use cookies for v1, note for v1.1 if analytics added). DPA: standard from Stripe/SendGrid."

### 13.7 — Security Expectations & Risk
- **Header:** Security
- **Mode:** text
- **Question:** What are security expectations? Encryption (data at rest, in transit)? Secrets management? Breach reporting? Insurance?
- **Options:** `free text` — Encryption (HTTPS only, AES256 at rest?), secrets (env vars, vaults), breach reporting (hours to notify, to whom), insurance carrier. Reason: Constrained by Phase 2 audience and risk tolerance.
- **Example:** "Standard SaaS security: HTTPS always, passwords hashed (bcrypt). Secrets in Azure Key Vault. Breach reporting: within 24 hours to customers + regulator (UK DPA requirements). No breach insurance (risk acceptable for v1)."
- **[TECH-OPEN:D11] skip in Customer mode** — encryption and secrets management are technical decisions; design-interrogation handles it.

### 13.8 — Brand & Legal Risk
- **Header:** Brand risk
- **Mode:** text
- **Question:** Trademark, domain ownership, brand guidelines? Legal risk (competitor claims, patent issues)?
- **Options:** `free text` — Trademark status (registered, pending, available), domain ownership, brand-use guidelines, known legal risks. Reason: Varies per product.
- **Example:** "Trademark 'Yardie' pending (applied Sept 2026; handled by legal team). Domain yardie.com: pending purchase. Brand guidelines: on-brand use defined in company manual. No known patent conflicts (landscape reviewed by legal, Oct 2026)."

---

## Phase 14 — Constraints, Operations & Support

**Rounds:** 4 rounds



### 14.1 — Budget, Deadline, Team
- **Header:** Constraints
- **Mode:** text
- **Question:** Budget (total to launch v1)? Deadline (target launch date)? Team size and skills available?
- **Options:** `free text` — Budget (£ or hours), launch target date, team (FTE: backend, frontend, QA, design, PM). Reason: Varies per product.
- **Follow-up rule:** Is the scope (Phase 5 MoSCoW) achievable in budget/timeline with this team? (If no, cut scope, grow team, or adjust deadline.)
- **Example:** "Budget: £80k. Deadline: Jun 2027 (6 months). Team: 3 backend (one part-time), 2 frontend (one part-time), 1 QA, 1 designer (external), 1 PM. Estimate: route assignment module ~4 weeks, mobile app ~6 weeks, testing ~3 weeks. Tight but doable if no surprises."

### 14.2 — Existing Stack & Hosting
- **Header:** Stack
- **Mode:** text
- **Question:** Current infrastructure, hosting, tech stack (from `tech-stack.md`)? Constraints or required platform choices?
- **Options:** `free text` — Hosting (AWS, Azure, on-premises), databases (PostgreSQL, SQL Server), frameworks (from tech-stack.md), existing systems to integrate. Reason: Constrained by org policy and tech-stack.md.
- **Example:** "AWS (existing account). PostgreSQL (org standard). .NET 10 / Blazor (from template). Azure AD for identity (already deployed). No on-premises; all cloud."

### 14.3 — Support Model & Tiers
- **Header:** Support
- **Mode:** choice
- **Question (Step 1):** Who provides support?
- **Options:**
  - *In-house team* → Your staff handles all support; full control, higher cost.
  - *Outsourced / vendor-managed* → Third-party support provider; lower cost, less control.
  - *Hybrid* → In-house L1 (triage), outsourced L2 (deeper troubleshooting).
- **Question (Step 2):** Support tiers & SLAs?
- **Options:**
  - *Free tier: best-effort support* → Email only, slow response; good for low-risk products.
  - *Single tier: SLA-backed support* → One tier with guaranteed response/resolution SLA; e.g., P1 4hr response, P2 1 day.
  - *Multiple tiers: free, standard, premium* → Free best-effort, standard SLA, premium priority; tiered pricing.
- **Follow-up rule:** If SLA mentioned: P1 (critical) response time? P2 (high) response time? Resolution SLA or response only? Uptime target (99.5%, 99.9%)?
- **Example:** "In-house: PM + 1 support engineer (rotating on-call). Tiers: Free tier (email, best-effort). Standard (v1.1, email + Slack, 24hr response). SLA: 99.5% uptime (maintenance 10 PM–6 AM UTC)."
- **Mapping:** Constrains Dimension 12 (Delivery, Environments & Hosting) in design-interrogation (support tooling, escalation process).

### 14.4 — Release Cadence & Rollback Plan
- **Header:** Releases
- **Mode:** text
- **Question:** How often will updates ship? (Weekly sprints, monthly releases, as-needed?) Rollback plan if production breaks?
- **Options:** `free text` — Release cadence (weekly, bi-weekly, monthly), deployment model (CI/CD, manual, phased rollout), rollback plan (database backup frequency, feature flags for safe rollback). Reason: Varies per org.
- **Example:** "Bi-weekly releases (Thursday evenings, UTC). Automated CI/CD (GitHub Actions). Rollback: database snapshots hourly, revert to previous Docker image. Feature flags for risky changes (canary rollout to 10% of users, monitor, then full rollout)."

### 14.5 — Analytics, Telemetry & Feedback Loops
- **Header:** Observe
- **Mode:** text
- **Question:** What metrics/events will you track? (From Phase 4 tracking plan.) Analytics tool? Crash reporting for native apps? User feedback collection?
- **Options:** `free text` — Events (login, route_assigned, sync_failed), tool (Mixpanel, Google Analytics, custom), crash reporting (Sentry, Crashlytics), feedback channel (in-app surveys, support email, NPS). Reason: Constrained by Phase 4 KPIs.
- **Example:** "Events: login, route_assigned, driver_location_sync, delivery_photo, support_contact. Tool: Mixpanel (track funnel from login → first assignment). Crash reporting: Sentry (mobile and web). Feedback: in-app NPS survey (monthly, 5 questions)."

### 14.6 — Performance & Sustainability Budgets
- **Header:** Performance
- **Mode:** text
- **Question:** Performance targets? (Load time, bandwidth, battery drain?) Sustainability or cost targets (carbon, cloud spend)?
- **Options:** `free text` — Load-time budget (First Contentful Paint, Time to Interactive), bandwidth cap (total transfers/month), battery drain (for mobile), cloud-cost envelope (e.g., "<£5k/month"). Reason: Varies per product.
- **Example:** "FCP <2s, TTI <4s (web). Page size <1MB. Mobile: <10MB app download, <20MB data/month syncing. Cloud budget: <£2k/month at 10k active users. Revisit if exceeds budget."

### 14.7 — Maintenance Ownership After Launch
- **Header:** Maintenance
- **Mode:** text
- **Question:** Who owns maintenance after v1 launch? (In-house team, vendor, hybrid?)
- **Options:** `free text` — Owner (team name, org), ongoing-maintenance tasks (bug fixes, security patching, OS updates, third-party library updates), release schedule (when can we pause for v2 planning?). Reason: Varies per org.
- **Example:** "In-house team (3 backend, 1 frontend, 1 QA rotating on-call). Maintenance: weekly patch Thursday evenings, urgent security fixes same day. Can pause new features for v2 planning once daily active users stabilise (target Sep 2027)."

---

## Phase 15 — Launch & Adoption

**Rounds:** 3 rounds



### 15.1 — Pilot / Beta Plan
- **Header:** Pilot
- **Mode:** choice
- **Question:** Launch approach?
- **Options:**
  - *Closed beta only* → Internal team, 1–2 weeks; find critical bugs before external launch.
  - *Open beta* → Sign-up; 2–4 weeks; real users, real-world feedback; grow early user base.
  - *Soft launch (quiet rollout)* → Gradual rollout by region/segment; watch metrics; scale carefully.
  - *Public launch immediately* → High risk; suitable for low-impact products only (e.g., content sites, free tools).
- **Escape options:** *Not sure yet* → Assumption; recommend open beta 2 weeks before full launch.
- **Follow-up rule:** Beta duration? Pilot user count / source? Success criteria (crash rate, sync error rate, NPS target, P1 bug limit)?
- **Example:** "Open beta 2 weeks (Jul 2027). Pilot: 50 managers from 5 test yards (existing customers, volunteer). Success: <1% crash rate, <2% sync errors, NPS >60, <5 P1 bugs. If met → full launch Aug 2027."
- **Mapping:** Constrains Phase 15 launch timeline and Phase 14 team readiness (support, monitoring).

### 15.2 — Launch Timing Drivers
- **Header:** Timeline
- **Mode:** text
- **Question:** What drives the launch date? (Market opportunity, competitor, internal deadline, feature completeness?)
- **Options:** `free text` — Driver (Q2 2027 fiscal target, competitor launching, customer event, feature-complete, team capacity), risk if delayed. Reason: Varies per product.
- **Example:** "Market driver: competitors shipping Oct 2026 (we need to launch before their advantage grows). Timeline: beta Jul, full launch Aug 2027. Risk: if delayed past Aug, first-mover advantage lost; revisit market window if slipping."

### 15.3 — Migration & Rollout (If replacement)
- **Header:** Migration
- **Mode:** text
- **Question:** (If Phase 0 flagged *Replacement / Migration*.) Parallel run with old system? Switch-over date? Rollback plan?
- **Options:** `free text` — Migration strategy (big bang, phased by region/segment, parallel run for N weeks), data validation before cutover, rollback plan. Reason: Varies per product.
- **Example:** "Phased rollout: yard 1 + 2 (test yards, first week Aug 2027). Monitor 1 week, then roll to remaining yards (week 2–3). Parallel run: old system accessible for 2 weeks post-launch (rollback if critical issue). Rollback: restore database from Aug-1 snapshot, run old app."

### 15.4 — Customer Onboarding & Training
- **Header:** Onboarding
- **Mode:** text
- **Question:** How will customers onboard to this product? (Self-service, dedicated trainer, webinars, documentation, all of the above?)
- **Options:** `free text` — Onboarding method (self-serve guide, 1-on-1 call, group webinar, in-person training), documentation (knowledge base, videos, checklists), success metric (% of users completing first task, avg onboarding time). Reason: Varies per product / audience.
- **Example:** "Self-serve onboarding (in-app tutorial, 15 min). Video walkthrough (5 min, available in help centre). Group webinar for new customers (60 min, recording available). 1-on-1 calls for Enterprise tier (optional). Success metric: 90% of managers complete first route assignment within 1 day."

### 15.5 — Marketing & Communications
- **Header:** Marketing
- **Mode:** text
- **Question:** How will you market / communicate the launch? (Social media, press release, email to existing customers, landing page, webinars, ads?)
- **Options:** `free text` — Channels (email, social media, press, webinars, ads), messaging (speed, cost savings, ease), audience (existing customers, new prospects, analysts). Reason: Varies per product.
- **Example:** "Email: announcement to 200 existing customers (early access). Landing page (product site). LinkedIn posts (targeting logistics directors). Webinar: 'Dispatch Faster' (60 min, Sep 2027). No paid ads for v1 (budget for v1.1). Press release: TechCrunch, LocalGov (if UK public sector interest)."

### 15.6 — Success Review & Post-Launch Cadence
- **Header:** Review
- **Mode:** text
- **Question:** When will you review launch success? (1 week, 1 month, 3 months?) What's the next milestone (v1.1, profitability, specific KPI target)?
- **Options:** `free text` — Review date (e.g., "30 days post-launch"), KPIs to hit (sign-ups, NPS, retention, revenue), next phase or go/no-go decision. Reason: Varies per product.
- **Example:** "Review at 30 days post-launch (Sep 1, 2027). Success metrics: >100 sign-ups, NPS >60, crash-free rate >95%. If met, proceed to v1.1 planning (Sep 15). If not, retrospective to understand why + corrective actions."

---

## Phase 16 — Risks, Assumptions, Dependencies

**Rounds:** 2 rounds



### 16.1 — Top Risks & Owners
- **Header:** Risks
- **Mode:** text
- **Question:** What are the top 3–5 risks to this product? (Technical, market, team, third-party.) For each: likelihood (high, medium, low), impact if realised (high, medium, low), mitigation, owner.
- **Options:** `free text` — Risk (e.g., "Google Maps ETA API goes down", "Yard managers reject new UI"), likelihood × impact, mitigation (what reduces the risk?), owner (who monitors / mitigates?). Reason: Unique per product.
- **Follow-up rule:** High likelihood + high impact = must mitigate before launch. Medium/medium = contingency plan. Low = monitor.
- **Example:**
  - "Risk 1: Google Maps API outage. Likelihood: low (Google 99.9% SLA). Impact: high (dispatch broken). Mitigation: local cache of routes + fallback to manual routing. Owner: backend engineer (test offline mode weekly). Status: medium risk, mitigated in Phase 11."
  - "Risk 2: Drivers don't adopt (revert to spreadsheets). Likelihood: high (change fatigue). Impact: high (product fails). Mitigation: 1-on-1 driver training, in-app onboarding, rapid bug-fix SLA. Owner: PM. Status: high risk, critical success factor."

### 16.2 — Assumptions to Validate
- **Header:** Assumptions
- **Mode:** text
- **Question:** What assumptions are you making? (About users, market, tech, team capability?) For each: validation method (how will you confirm it?) and date (when will you know?).
- **Options:** `free text` — Assumption (e.g., "drivers will use the app if it syncs within 5 sec"), how to validate (user test, analytics, survey, beta feedback), target date. Reason: Logged to ensure they are revisited.
- **Example:**
  - "Assumption 1: Yard managers value real-time updates over detailed forecasting. Validate: Phase 11 prototype walkthrough + beta user feedback (target Jul 2027). If wrong, pivot to predictive features (v1.1 decision)."
  - "Assumption 2: 20% growth in 3 years is achievable. Validate: market analysis (competitor growth), pilot sign-up velocity (Jul 2027). If < 5% month-on-month growth in first 2 months, revise forecast."

### 16.3 — External Dependencies
- **Header:** Dependencies
- **Mode:** text
- **Question:** What external dependencies could block or delay this product? (Third-party APIs, vendor contracts, regulatory approval, team dependencies, other projects.)
- **Options:** `free text` — Dependency (e.g., "Google Maps API approval", "vendor contract renewal"), criticality (blocker, high, medium, low), owner, target date. Reason: Unique per product.
- **Example:**
  - "Dependency 1: Google Maps API (production key approval). Owner: backend engineer. Critical: blocker. Target date: Jun 2027 (1 month before launch)."
  - "Dependency 2: Azure AD team to configure org integration. Owner: IT. Critical: high (blocks enterprise customers). Target: Jun 2027."
  - "Dependency 3: Legal review of privacy policy. Owner: legal team. Critical: medium (can defer 2 weeks). Target: Jul 2027."

---

## Phase 17 — Completeness Check, Readback & Sign-Off

**Rounds:** 1 round (checklist, readback, sign-off)



(No new questions; this phase is a coverage check and final approval.)

### 17.1 — Coverage Checklist
- **Header:** Coverage
- **Mode:** choice
- **Question:** Coverage check: are there any areas with gaps, assumptions, still deferred, or needing rework?
- **Procedure:** Pre-fill each area's status from the discovery log (Resolved / Assumption / Deferred / Conflict / N-A). Ask multi-select over <=4 rounds: "Which of these have open items?" (<=4 areas per round).
- **Options (multi-select, 4 rounds):**
- **Round 1 — Intake & Problem (4 areas):**
  - *Intake & governance* — Respondent mode, decision rights, AI flag. Phase 0.
  - *Problem & opportunity* — Problem statement, timing, cost. Phase 1.
  - *Audience* — 3 segments ranked, demographics, geography, motivation, brand fit. Phase 2.
  - *Users & personas* — 4 personas, jobs-to-be-done, context. Phase 3.
- **Round 2 — Value & Scope (4 areas):**
  - *Value & success* — KPIs, tracking methods, v1 definition of done. Phase 4.
  - *Scope* — MoSCoW (Must/Should/Could/Won't), MVP boundary, release plan. Phase 5.
  - *Market & business* — Competitors, revenue model, pricing, tenancy, white-label. Phase 6.
  - *Journeys & features* — Top 5 journeys, integrations, import/bulk, UGC, AI sub-block (if present). Phase 7.
- **Round 3 — UX/UI & Platforms (4 areas):**
  - *UX (wireframes approved)* — IA, screens, onboarding, forms, feedback, notifications, a11y, responsive. Phase 8.
  - *UI (mockups approved)* — Brand, colour, typography, themes, density, icons, motion, deliverables. Phase 9.
  - *Platforms & deliverables* — Web/iOS/Android/Windows/macOS, feature parity, DLV register, API, admin portal. Phase 10.
  - *Prototype (walkthrough done)* — Clickable prototype, validation-log filled. Phase 11.
- **Round 4 — Data, Compliance & Operational (4 areas):**
  - *Data & integrations* — Data ownership, migration, third parties (Stripe, Auth0, Maps, email/SMS), content ownership. Phase 12.
  - *Compliance & legal* — GDPR, industry regs, a11y law, T&Cs, privacy, security, brand risk. Phase 13.
  - *Operations & support* — Budget, deadline, team, stack, support model, release cadence, analytics, sustainability. Phase 14.
  - *Launch & adoption* — Pilot plan, launch drivers, migration, onboarding, marketing, review cadence, rollback. Phase 15.
  - *Risks & assumptions* — Top risks, assumptions to validate, dependencies. Phase 16.
  - *Completeness (Phase 17)* — Overall status (Draft / Confirmed / Blocked).
- **Follow-up rule:** For each area marked as having open items: what's missing? Who owns closing it? Target date?

### 17.2 — Full Readback & Confirmation
- **Header:** Sign-off
- **Mode:** choice
- **Question:** (Presented as a 5–10 min summary.) "This is what we will build: [summary of problem, audience, journeys, platforms, deliverables, timeline, budget, success metrics]. The prototype shows the UX. Top risks are [risk1, risk2]. Key assumptions to validate: [assumption1]. Correct?"
- **Options:** (Fixed reaction set)
  - *Correct, let's proceed* → Proceed to finalisation; sign-off recorded.
  - *Mostly correct; I'd change [text]* → Capture the change, amend the brief, re-confirm.
  - *No, we need to rethink [area]* → Return to the affected phase; re-interview. Record as Major Rethink in Phase 17 status.
- **Mapping:** Recorded as final sign-off decision, approved by decision owner (Phase 0 identified).

---

## Fixed Reaction Sets (All Phases)

Used in mockup/prototype show-backs and final confirmation:

**Design Reaction:**
- *Accept* — Approved as-is.
- *Change* (free text: what to change) — Approved with noted changes; revise and re-show.
- *Reject* — Not approved; major rethink.
- *Question* — Unclear; flagged for later resolution.

**Task Validation Reaction:**
- *Succeeded* — Task completed as expected.
- *Struggled* — Completed but with difficulty / confusion; capture observation.
- *Failed* — Could not complete; blocker or misunderstanding; capture observation.

**Playback Reaction:**
- *Correct* — Summary accurate.
- *Mostly with changes* (free text) — Summary mostly accurate; noted changes to confirm.
- *No, redo this* — Inaccurate; return to phase and re-interview.

---

## Lettered-List Fallback (For clients without choice tools)

When the skill cannot use `AskUserQuestion` (e.g., Copilot, plain chat), render options as lettered lists:

```
**Question:** [Question text]

A. [Option 1 label: description]
B. [Option 2 label: description]
C. [Option 3 label: description]
D. [Option 4 label: description]
E. Other: [free text]

Reply A, B, C, D, E, or type your own answer.
```

Parsing: A/B/C/D mapped to option indices; E or freeform text captured as *Other / free input*.

---

## Follow-Up Rule (General)

Every answer is checked for four dimensions **before the phase closes**:

1. **Number** — If a metric or quantity is reasonable, ask for numbers. *"How many?" "What is the cost?"*
2. **Named Owner** — If a decision or task is stated, ask who owns it. *"Who makes this call?" "Who tracks this metric?"*
3. **Example** — If vague, ask for a concrete example. *"Can you give me an example of a [feature / use case / audience]?"*
4. **Exception** — If a rule is stated broadly, ask when it doesn't apply. *"Are there cases where [rule] doesn't hold?"*

Missing any → open follow-up before the phase closes. Unanswered follow-ups escalate to Phase 16 (Risks, Assumptions, Dependencies) as *Deferred* or *Assumption*.

---

## Progress Line Format

Display each round:
```
Phase N of 18 — {Phase Name} · About X rounds left · (Pause and save / Skip this phase)
```

Example:
```
Phase 3 of 18 — Users & Personas · About 2 rounds left · (Pause and save / Skip this phase)
```

---

## Final Completeness Checklist (Phase 17)

| Area | Status | Details | Owner |
|---|---|---|---|
| Problem & opportunity | Resolved / Assumption / Deferred / Conflict | Resolved: Problem statement, pain, cost, timing clear. | PM |
| Audience | Resolved / ... | Resolved: 3 segments defined, demographics, geography, motivation, brand fit. | PM + user research |
| Users & personas | Resolved / ... | Resolved: 4 personas with jobs-to-be-done, context. | PM + design |
| Value & success | Resolved / ... | Resolved: 5 KPIs, tracking methods, v1 definition of done. | PM + metrics owner |
| Scope (MoSCoW, MVP) | Resolved / ... | Resolved: 15 features, Must/Should/Could/Won't, MVP confirmed, timeline fits budget. | PM + tech lead |
| Competitors & revenue | Resolved / Assumption | Resolved or Assumption if market unvalidated. | PM + business |
| Journeys & features | Resolved / ... | Resolved: 5 top journeys, AI sub-block (if present), integrations. | PM + design + backend |
| UX (wireframes) | Resolved / ... | Resolved: IA, 10 key screens, states, onboarding, accessibility. Wireframes approved. | Design |
| UI (mockups) | Resolved / ... | Resolved: brand, colour, typography, themes, density, icons, motion. Mockups approved. Tokens generated. | Design |
| Platforms & deliverables | Resolved / ... | Resolved: web/mobile/desktop specs, API, SDK, docs, admin portal, DLV register. | Architect + PM |
| Prototype | Resolved / ... | Resolved: Clickable prototype from approved mockups. Walkthrough & validation completed. | Designer + developer |
| Data & integrations | Resolved / ... | Resolved: Data ownership, migration, third parties (Stripe, Auth0, Maps), content ownership. | Backend + PM |
| Compliance & legal | Resolved / Assumption | Resolved or Assumption if legal review deferred. GDPR, industry regs, accessibility law, T&Cs/privacy. | Legal + compliance |
| Operations & support | Resolved / Assumption | Resolved: Budget fits scope, team skills confirmed, SLA defined, release cadence. | PM + tech lead |
| Launch & adoption | Resolved / Deferred | Resolved: Pilot plan, onboarding, marketing, review cadence. (May defer timing to Phase 17). | PM + marketing |
| Risks & assumptions | Resolved / Deferred | Resolved or Deferred: Top risks, assumptions to validate, dependencies tracked. | PM + tech lead |
| **Overall** | **Draft / Confirmed / Blocked** | Draft: approved by decision owner, ready for design-interrogation. Confirmed: signed off. Blocked: unresolved issue. | Decision owner |

---

## Notes for the Skill Implementation

1. **Translation:** Questions are asked in the respondent's language (English or Dutch instructions; skill translates). Option labels and descriptions should be short enough to translate without bloat.

2. **Option set reuse:** All questions and option sets are curated here; the skill reads this file on each run and reuses option sets so answers are consistent across sessions.

3. **Resumability:** If a session is paused, the skill checks for an existing `docs/product/discovery-decisions.md` and offers: resume (continue from where you left off), amend (change an earlier answer), or start over. Resumed sessions re-ask only the missing phases.

4. **Pre-filled answers:** When a value can be inferred (Phase 0 reads `docs/input/` files, Phase 2 reads audience research if provided, Phase 10 reads `tech-stack.md` for platform defaults), the skill proposes it as the first option labelled *(from {source})*. One-click confirmation is faster than re-entering.

5. **Free text handling:** Every choice question includes *Other* as the final option. If the respondent types a freeform answer (not matching any option), it is recorded verbatim and, if needed (e.g., platform name), normalised with the respondent's confirmation in a follow-up.

6. **Decision IDs:** Each resolved answer becomes a `PD-nnn` decision logged to `docs/product/discovery-decisions.md` immediately (progressive capture). Deferred answers and assumptions are also logged with status and target date.

7. **Mapping to downstream:** Each option set includes metadata on how the answer maps to a decision status (Resolved/Assumption/Deferred/Conflict/N-A) and a downstream constraint (e.g., Phase 2 audience → Phase 8 UX density and Phase 9 typography; Phase 7 journeys → Phase 10 deliverables).

8. **Neutral language:** Questions and options avoid solutioneering (no "should it be an app?" before problem and audience are settled). Options are ordered by likelihood, not by bias. Recommendations are provided only for decisions, never for facts.

---

End of Question Bank. See `output-templates.md` for document templates and metadata structure.
