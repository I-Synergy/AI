# Product Discovery — Output Templates

Markdown templates for all six discovery documents plus prototype walkthrough and validation log. Use these as scaffolds; the skill populates them with answers from each phase. Replace `{...}` placeholders with actual values.

All documents start with: **Status** (Draft / Confirmed), **Respondents**, **Last updated**.

---

## Template 1: product-brief.md

Location: `docs/product/product-brief.md`

Primary consumer: `design-interrogation` Phase -1 (pre-resolved input).

```markdown
# Product Brief: {Product Name}

**Status:** Draft  
**Respondents:** {Name} ({role}); {Name} ({role})  
**Last updated:** {date}  
**Open items:** {List of unresolved questions or assumptions needing validation}

## Product Type

**Origin:** {Greenfield / Extending / Replacing / Internal tool}

**Orientation:** {B2C / B2B / B2E / B2G / Platform/API}

## Vision & Problem Statement

**Problem:** {Problem statement from Phase 1.1}

**For whom:** {Target audience segments from Phase 2.1, ranked}

**Why now:** {Reason for timing from Phase 1}

**Evidence:** {Research type and date; what is known vs. guessed}

## Current System (if Replacing or Extending)

**Pain points:** {Major issues with existing system}

**Must-keep features:** {Functionality that cannot be removed}

**Current UI inventory:** {Link to screenshot or summary of existing interface}

## Value & Success

**Value proposition (per segment):**
- {Segment 1}: {Quantified value from Phase 4.1}
- {Segment 2}: {Quantified value}

**Business goals (GL-nnn):**
- GL-001: {Goal}, measured {method}, target {number} by {date}
- GL-002: {Goal}, measured {method}, target {number} by {date}

**Key metrics & tracking plan:**
| Metric | Goal | Measurement method | Owner | Frequency |
|---|---|---|---|---|
| {KPI 1} | {Target} | {Event/survey/manual} | {Owner} | Daily / weekly / monthly |
| {KPI 2} | {Target} | {Event/survey/manual} | {Owner} | Daily / weekly / monthly |

**Definition of done for v1:** {Acceptance criteria from Phase 4.4}

## Scope & Release Plan

**MoSCoW prioritisation (Phase 5.1):**

| Priority | Feature/Capability | Rationale |
|---|---|---|
| **Must** | {Feature 1} | Core, v1 blocker |
| **Must** | {Feature 2} | Core, v1 blocker |
| **Should** | {Feature 3} | High priority, v1.1 acceptable if squeezed |
| **Could** | {Feature 4} | Nice-to-have, v2+ |
| **Won't** | {Feature 5} | Explicit out-of-scope; revisit v2 |

**MVP (v1.0):** {List of Must + critical Should features}

**Release plan:**
- **v1.0 ({Date}):** {Features}
- **v1.1 ({Date}):** {Features}
- **v2.0 ({Date or TBD}):** {Features}

**Kill criteria:** {Condition under which product is paused/cancelled}

## Market & Business Model

**Competitive landscape:**
| Competitor | What they do | Our differentiation |
|---|---|---|
| {Competitor 1} | {Offering} | {How we are different} |
| {Competitor 2} | {Offering} | {How we are different} |

**Revenue model:** {From Phase 6.2}

**Pricing:** {Subscription price, freemium tiers, or one-time cost}

**Monetisation mechanics (Phase 6.3):**
- Payment provider: {Stripe / PayPal / invoice / in-app purchase}
- Billing frequency: {Monthly / annual / one-time}
- Tax/VAT: {Jurisdiction, applicable rate}
- App-store commercial rules: {E.g., "Apple takes 30% on IAP"}

**Tenancy model:** {Single-tenant / multi-tenant / self-hosted}

**White-label / reseller:** {Direct / reseller channel / white-label}

## Journeys & Functional Needs

**Top journeys (Phase 7.1):**

1. **{Journey name}**
   - **Trigger:** {Event that starts the journey}
   - **Steps:** {1. ... → 2. ... → 3. ...}
   - **Outcome:** {What changes}
   - **Edge cases:** {E.g., "driver already assigned", "offline during sync"}

2. **{Journey name}**
   - **Trigger:** {...}
   - **Steps:** {...}
   - **Outcome:** {...}

**Notifications & reporting (Phase 7.2):**
- Push events: {Event triggers, frequency}
- E-mail: {Frequency, digest or real-time}
- SMS: {Yes/No, use cases}
- Reports: {Types, frequency, export format}

**Import/bulk operations (Phase 7.3):**
- {Bulk operation type} (e.g., "CSV driver import"): {Volume}, {Frequency}, {Error handling}

**User-generated content (Phase 7.4):**
- {UGC type, e.g., "delivery notes"}: {Moderation policy}

**AI/ML features (Phase 7.5, if present):**
- **Use case:** {What the AI does}
- **Data:** {What is fed to the model}
- **Acceptable error rate:** {Tolerance, fallback behaviour}
- **Human oversight:** {Required / recommended / none}
- **Transparency:** {Show "AI-generated" label or hide}
- **Cost:** {Per-call cost, estimated monthly}
- **EU AI Act risk class:** {If applicable}

## Data, Content & Integrations

**Data ownership:** {Phase 12 decision on who owns what}

**Data migration:** {If applicable, strategy and timeline}

**Third-party integrations:** {List of required APIs, services, dependencies}

**Analytics & reporting:** {Event tracking plan, reporting frequency}

## Compliance, Legal & Regulatory Register

**GDPR/Data protection:** {Applicable jurisdictions and obligations}

**Industry-specific rules:** {HIPAA, PCI-DSS, accessibility law, etc.}

**Accessibility compliance:** {WCAG AA / AAA / EN 301 549 / EAA level}

**Audit & licensing:** {Required audits, third-party certifications}

**Terms of service & privacy:** {Status: {EXAMPLE - replace with actual status}}

## Constraints, Operations & Support

**Budget:** {Total allocated}

**Timeline:** {Launch target date}

**Team:** {Size and roles}

**Technology stack:** {Framework/database recorded as [TECH-OPEN] for design-interrogation}

**Support model:** {Self-serve / email / chat / phone}

**Release cadence:** {Weekly / monthly / per-feature}

**SLA & monitoring:** {Uptime target, monitoring tools}

**Sustainability:** {Maintenance plan post-launch}

## Launch & Adoption Plan

**Pilot/beta (Phase 15.1):**
- **Approach:** {Public beta / closed beta / soft launch}
- **Users:** {Number of beta users, selection criteria}
- **Duration:** {Dates}
- **Success criteria:** {KPIs for go/no-go decision}

**Launch date drivers (Phase 15.2):**
- {Reason for launch timing}

**Migration/rollout (Phase 15.3, if replacement):**
- **Strategy:** {Big bang / phased by region / parallel run}
- **Rollback plan:** {Database snapshot frequency, restoration steps}

**Customer onboarding (Phase 15.4):**
- **Methods:** {Self-serve guide, webinars, 1-on-1 calls}
- **Success metric:** {% users completing first task within X time}

**Marketing & communications (Phase 15.5):**
- **Channels:** {Email, social media, press, webinars, ads}
- **Messaging:** {Key value propositions}
- **Audience:** {Existing customers, new prospects, analysts}

**Success review (Phase 15.6):**
- **Review date:** {Date for launch retrospective}
- **Metrics to hit:** {Sign-ups, NPS, retention, revenue targets}
- **Next milestone:** {v1.1, profitability target, specific KPI}

## Risks, Assumptions, Dependencies

**Top risks (Phase 16.1):**

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | {Risk description} | High / Med / Low | High / Med / Low | {How to reduce risk} | {Owner} |
| 2 | {Risk description} | High / Med / Low | High / Med / Low | {How to reduce risk} | {Owner} |

**Assumptions to validate (Phase 16.2):**

| # | Assumption | Validation method | Target date |
|---|---|---|---|
| 1 | {Assumption} | {User test / beta feedback / survey / analytics} | {Date} |
| 2 | {Assumption} | {User test / beta feedback / survey / analytics} | {Date} |

**External dependencies (Phase 16.3):**

| Dependency | Criticality | Owner | Target date |
|---|---|---|---|
| {Dependency, e.g., "Google Maps API approval"} | Blocker / High / Medium / Low | {Owner} | {Date} |
| {Dependency} | ... | ... | ... |

## Stakeholders & Decision Rights

| Role | Name | Decision area | Contact |
|---|---|---|---|
| {Role, e.g., CEO} | {Name} | Scope, budget, go/no-go | {Email/phone} |
| {Role, e.g., Design Lead} | {Name} | Visual design, UX | {Email/phone} |
| {Role} | {Name} | {Area} | {Email/phone} |

**Sign-off:** This brief was reviewed and approved by {Decision owner name} on {Date}.

---

**Confidentiality notice:** This document contains commercial information including product strategy, pricing, roadmap, and user research. It is intended for team members and trusted stakeholders. Do not share publicly without explicit approval. Check repository visibility before committing to version control.

**Personas:** All personas are fictional composites based on research, not real people. No personally identifiable information is included.
```

---

## Template 2: audience-profile.md

Location: `docs/product/audience-profile.md`

Primary consumers: `ux-brief.md`, `ui-design-brief.md`, `design-interrogation` Dimensions 7 and 9.

```markdown
# Audience Profile

**Status:** Draft / Confirmed  
**Respondents:** {Names and roles}  
**Last updated:** {Date}  
**Open items:** {Unresolved audience questions}

## Audience Segmentation

**Primary segment:** {Segment 1 name}  
**Secondary segment:** {Segment 2 name}  
**Tertiary segment:** {Segment 3 name (if applicable)}

| Rank | Segment | Size (now) | Size (3 years) | Role |
|---|---|---|---|---|
| 1 (Primary) | {SEG-001 Segment name} | {#} | {#} | Who buys / uses / decides |
| 2 (Secondary) | {SEG-002 Segment name} | {#} | {#} | Who buys / uses / decides |
| 3 (Tertiary) | {SEG-003 Segment name} | {#} | {#} | Who buys / uses / decides |

---

## Detailed Segment Profiles

### Segment 1: {Segment name} (SEG-001)

**Type & demographics:**
- Type: {B2C / B2B / B2E / B2G / mixed}
- Age range: {e.g., 28–55}
- Role/profession: {e.g., Logistics supervisor, fleet manager}
- Education: {High school / diploma / university}
- Income band: {e.g., £30–60k (if pricing relevant)}

**Geography & language:**
- Countries/regions: {e.g., UK only}
- Languages: {E.g., English primary, Dutch secondary (v1.1)}
- Reading level: {Plain English / technical language OK / specialized jargon}
- Cultural conventions: {Date format, colour meaning, RTL, taboos}
- Legal jurisdiction: {GDPR / other data protection}

**Digital skill & habits:**
- Tech literacy: {Power user / proficient / learning / not-tech-focused}
- Familiar with comparable products: {Yes, which? / No}
- Daily apps used: {E.g., Slack, Google Sheets, Outlook}
- Patience for onboarding: {E.g., 20 min if it saves time daily}
- Preferred interface style: {Formal / friendly / visual / text-dense}

**Devices & connectivity:**
- Devices owned/used: {iPhone 12/13 (iOS 16+), shared iPad, Windows laptop}
- OS/browser mix: {iOS 16+, Android 11+, Chrome, Safari}
- Screen sizes: {E.g., phone 5–6", tablet 10", desktop 24"}
- Bandwidth: {Always online / 4G+WiFi mix / often offline}
- Offline periods: {Frequent / occasional / never}

**Context of use:**
- Location: {Office / field / vehicle / home / multiple}
- Single-handed use: {Yes / occasionally / no}
- Interruptions: {Frequent / occasional / rare}
- Session length & frequency: {E.g., 2–10 min, 20+ times/day}
- Shared devices: {Yes, managed/locked-down / no}

**Accessibility & inclusion:**
- Accessibility needs (estimated % of segment): {<5% / 10–20% / >20%}
- Specific needs: {Visual, hearing, motor, cognitive}
- Legal obligation: {WCAG AA / AAA / EN 301 549 / EAA}
- Assistive technology: {Screen reader / zoom / voice / switch / reduced-motion / colour-blindness}

**Motivation & emotion:**
- Why they come: {E.g., save time, reduce errors, comply with rules}
- What frustrates them today: {E.g., spreadsheet chaos, driver confusion}
- Stress level of the task: {High (critical) / medium / low}
- Desired tone/feeling: {Calm / playful / fast / authoritative / premium}
- Trust sensitivity: {High (payment, health, safety) / medium / low}

**Brand & voice fit:**
- Formality: {Formal / casual / friendly}
- Humour allowed: {Yes / no / situational}
- Brand personality: {E.g., professional, transparent, no-nonsense}
- Competitors they admire: {E.g., Slack (clean), Stripe (elegant)}
- Competitors they dislike: {E.g., TikTok (too casual)}

**Safeguarding & access:**
- Minors: {Yes, parental consent required / no}
- Vulnerable people: {Yes, duty of care required / no}
- Safety-critical use: {Yes, health/finance/driving / no}

**Evidence & confidence:**
| Finding | Source | Date | Confidence |
|---|---|---|---|
| {E.g., "20% of segment uses iPhones"} | User interviews (5 managers) | Sept 2026 | Known |
| {E.g., "Estimated 20% growth in 3 years"} | Market analysis (guess) | Oct 2026 | Assumption — validate via beta |

### Segment 2: {Segment name} (SEG-002)

[Repeat same structure as Segment 1]

---

## Audience → Design Traceability Table

How each audience finding constrains UX and UI decisions (canonical 8-row table referenced in all design briefs):

| Audience finding | Constrains | Phase + Decision |
|---|---|---|
| Low digital skill / older users | Larger type, plain language, fewer choices/screen, guided onboarding, visible labels over icons | Phase 8–9: 16px body, sans-serif, label all icons, simple navigation |
| Mixed / poor connectivity, field use | Offline-first, sync-conflict policy, small payloads, large touch targets, high-contrast outdoor theme | Phase 8–9: responsive, offline mode, 48px+ targets; Phase 10: offline-capable |
| Internal power users | Dense layouts, keyboard shortcuts, bulk actions, desktop-first | Phase 8–9: keyboard-first nav, bulk import UI, compact density |
| Many languages / RTL | Localisation architecture, layout mirroring, text-expansion room | Phase 8–9: 15% padding, RTL support if applicable |
| High accessibility need / legal duty | WCAG level, assistive-tech test matrix, reduced-motion and high-contrast themes | Phase 9: high-contrast theme, focus visible, test with screen readers |
| Trust-sensitive task | Tone, confirmation patterns, security cues, undo and reassurance copy | Phase 8–9: confirmations on destructive actions, security labels, undo available |
| Locked-down corporate devices | Installer type, admin rights, auto-update path, browser baseline | Phase 10: MSIX/DMG, auto-update, no elevation required |
| Minors or vulnerable users | Consent flows, content rules, data minimisation, moderation | Phase 13: consent UI, moderation policy, data retention limits |

---

End of Audience Profile. See `ux-brief.md` for UX-specific design decisions and screen inventory.
```

---

## Template 3: ux-brief.md

Location: `docs/product/ux-brief.md`

Primary consumers: Designer, UI developer, user-story skill.

```markdown
# UX Brief

**Status:** Draft / Confirmed  
**Respondents:** {Names}  
**Last updated:** {Date}  
**Open items:** {Unresolved UX questions}

## Design Implications of the Audience

See the 8-row canonical traceability table in `audience-profile.md` — refer to that instead of maintaining a copy here.

## Personas

Built from Phase 3 users and Phase 2 audience segments:

### Persona 1: {Name}

- **Role:** {E.g., Dispatch Manager}
- **Segment:** {SEG-001}
- **Primary job:** {E.g., Assign drivers to routes, ~45 min daily}
- **Context:** Desk + field, frequent interruptions, 20+ brief sessions/day
- **Frustration:** Spreadsheet chaos, driver confusion, slow updates
- **Motivation:** Save time, reduce errors, visible driver status
- **Tech proficiency:** Proficient (Slack, Sheets, Gmail daily); no patience for onboarding
- **Devices:** iPhone + Windows laptop + shared iPad in office
- **Accessibility:** None stated; vision normal, no mobility issues
- **Quote:** "I need to know where every driver is in 10 seconds, not 10 minutes."

### Persona 2: {Name}

[Repeat structure for each persona]

---

## Information Architecture & Navigation

**Mental model:** {E.g., "By role (dispatcher, driver, admin)"; "By time (today's tasks, this week, history)"; "By location (yard, zone, vehicle)"}

**Primary navigation:** {Tabs / sidebar / hamburger / breadcrumbs}

**Navigation diagram (ASCII):**

```
Web (Desktop):
  [Logo]           [Drivers] [Routes] [Reports] [Admin] [Account ▼]
                        ↓
                   Drivers (list + filters)
                   - Search / filter by zone, status
                   - Bulk assign, on leave
                   - Click for detail (photo, phone, stats)

Mobile:
  [Dispatch] [List] [Map] [Menu]
       ↓
  Dispatch board (cards, drag-drop to routes)
```

**Cross-surface consistency:** {What's identical web/mobile/desktop vs. platform-idiomatic}

---

## Key Screens & States (Screen Inventory)

Every screen gets an ID (`SCR-nnn`) for traceability in phase 17 completeness check and product spec.

| SCR ID | Screen name | Purpose | Persona | Journey | States | Components | Notes |
|---|---|---|---|---|---|---|---|
| SCR-001 | Route Assignment Board | Assign drivers to routes, drag-drop interaction | Alice (dispatcher) | Assign routes | empty, loading, success, error, offline | List, Card, DragDrop, Button | Core feature, high traffic |
| SCR-002 | Driver Profile | View driver details, contacts, status, history | Alice, Bob (admin) | N/A (support) | success, not-found, no-permission | Form, Table, Button, Link | Optional avatar (v1.1) |
| SCR-003 | Task List (Driver View) | Driver sees assigned tasks, mark complete, photos | Driver (secondary) | Accept & complete task | empty, loading, success, offline | List, Button, Camera, Timestamp | Mobile-first design |
| SCR-004 | Error: Sync Failed | Shown when offline sync has conflicts | Alice | (exception state) | conflict detail, retry button | Modal, Button, Text | Rare; reassurance copy needed |
| SCR-005 | Onboarding: Welcome | First-run experience for new dispatcher | Alice | (setup) | success | Hero image, CTA button, skip link | Contextual help, <2 min duration |

---

## Content & Tone of Voice

**Tone:** {E.g., professional, no jargon, direct, urgent (not formal)}

**Copy ownership:** {PM writes; design team reviews; legal approves}

**Examples:**
- Button: "Assign to route" (action-oriented, not "Complete assignment")
- Error: "Can't sync right now. Changes saved; we'll upload when online." (reassuring, not "Sync error 504")
- Help: "Drivers see this route when you hit Send." (simple, not "Broadcast route assignment to connected mobile clients")

**Help centre / documentation:**
- Platform: {Zendesk / self-hosted markdown / Intercom}
- Owner: {PM}
- Localisation: {English + Dutch (v1.1)}

---

## Forms & Validation

**Validation style:** {Real-time with inline error / blur / submit}

**Example: Create Driver form**
- **Name:** Required, real-time validation (feedback: "Name required")
- **Phone:** Optional, blur validation (feedback: "Invalid phone format")
- **Email:** Optional, blur validation + verification (feedback: "Check your inbox to verify email")
- **Submit:** Enabled once name + one contact filled

---

## Feedback, Undo & Reassurance

**Action confirmation:**
- Assign route: Inline success toast (3 sec, green) — "Assigned to route. Undo?"
- Unassign: Confirmation modal — "Remove driver from route? They'll lose all tasks."
- Delete driver: Confirmation modal + email confirmation sent — "Driver deleted. Cannot undo."

**Undo scope:** 5 min from action; older actions shown in history (not truly undoable).

**Destructive action warning:** Yes, modal confirmation required for delete, unassign, bulk actions.

---

## Notifications & E-mail Design

**In-app notifications (toast):**
- Route assigned: "Route assigned. Undo?" (3 sec, green)
- Sync error: "Can't sync right now. Retrying..." (persistent, yellow, auto-retry)
- Delivery complete: "Delivery confirmed." (3 sec, green)

**Push notifications:**
- Route assigned: Title "New route", Body "Alice assigned you 3 stops in zone A"
- Sync failed: Title "Sync failed", Body "Tap to retry"
- Frequency: Real-time for time-critical events; no more than 3/hour outside critical hours

**E-mail notifications:**
- Frequency: Daily summary (6 PM UTC) of exceptions and completions
- Template: {HTML + plain text} with unsubscribe link, company logo, branding
- Do-not-disturb: No notifications 10 PM–6 AM

**SMS:** {Not for v1; cost prohibitive; defer to v1.1 if needed}

---

## Accessibility & Localisation

**WCAG target:** WCAG AA (from Phase 2)

**Accessibility specifics:**
- Focus order: Logical left-to-right, top-to-bottom on all screens
- Labels: All form inputs + buttons labelled (visible or aria-label)
- Keyboard navigation: Tab, Enter, Escape, arrow keys fully functional
- Screen reader: Tested with NVDA and JAWS on Windows, VoiceOver on macOS/iOS
- Reduced motion: Animations disabled if `prefers-reduced-motion` set; static fallback
- Colour contrast: All colour pairs checked against WCAG AA (minimum 4.5:1 text, 3:1 UI components)
- Target size: Buttons and interactive elements ≥44px (iOS), ≥48px (Android), ≥44px (web desktop)

**Localisation (Phase 8.8):**
- Languages for v1: English + Dutch (both full-featured)
- RTL: No (English + Dutch are LTR)
- Text expansion room: German ~15% longer (left 15% padding in English copy)
- Formats: Date DD/MM/YYYY, number 1,000.00, currency £

**Date/time handling:** UTC in backend; display in local timezone per device setting; user can override timezone in preferences.

---

## Responsive Design & Devices

**Breakpoints:**

| Breakpoint | Width | Layout | Use cases |
|---|---|---|---|
| Mobile | < 600px | Single column, full-width content, bottom tab bar | Phone (portrait + landscape) |
| Tablet | 600–900px | Left sidebar collapsible, main area flexes, top nav optional | Tablet (portrait + landscape) |
| Desktop | > 900px | Persistent sidebar, resizable, keyboard nav | Windows + macOS + web browsers |

**Responsive behaviour (ASCII):**

```
Mobile (< 600px):       Tablet (600–900px):         Desktop (> 900px):
┌──────────────┐        ┌────────┬──────────┐        ┌──────────┬──────────┐
│   [Header]   │        │[Sidebar][Content  │        │[Sidebar]│[Content]  │
├──────────────┤        │───────── ]        │        │─────────┼──────────│
│              │        │         [Content]  │        │         │[Content] │
│  [Content    │        │         ┴──────────┤        │         │          │
│   Full w]    │        └────────┴──────────┘        └─────────┴──────────┘
├──────────────┤
│ [Tabs] ▪ ▪ ▪ │
└──────────────┘
```

**Device support (from Phase 10):**
- iPhone 12+ (portrait + landscape)
- iPad 7th gen+ (portrait + landscape, large targets)
- Android phones (Samsung, Pixel, OnePlus; 6–7" screens)
- Android tablets (10–12"; landscape primary for dispatch)
- Windows desktop (1920x1080 minimum; larger screens supported)

---

## Research & Evidence

| Area | Evidence type | Date | Confidence |
|---|---|---|---|
| Information architecture | 5 user interviews + card-sort exercise | Sept 2026 | Known |
| Top journeys | Current system observation + interviews | Sept 2026 | Known |
| Onboarding depth | Internal staff testing + competitor analysis | Oct 2026 | High confidence |
| Keyboard-first preference | Power user interviews (internal team) | Oct 2026 | Known for segment 2 |

---

End of UX Brief. See `ui-design-brief.md` for visual design decisions and component library details.
```

---

## Template 4: ui-design-brief.md

Location: `docs/product/ui-design-brief.md`

Primary consumers: Designer, theme-generator skills, UI developer.

```markdown
# UI Design Brief

**Status:** Draft / Confirmed  
**Respondents:** {Names}  
**Last updated:** {Date}  
**Open items:** {Unresolved design questions}

## Design Implications of the Audience

See the 8-row canonical traceability table in `audience-profile.md`.

## Brand & Visual Identity

**Existing brand assets:**
- Figma: {Link to shared file, if any}
- Logo: {Link to SVG / file}
- Design system: {URL or "none"}
- Brand guidelines: {URL or "internal document"}

**Brand personality:** {E.g., Professional, transparent, no-nonsense; no playful humour}

**Visual references:** {Competitors/apps they admire: "Slack's clean look, Stripe's elegance, avoid TikTok vibe"}

---

## Colour & Theme

**Primary accent colour:** {HEX or HSL, e.g., #0078D4 (Microsoft Blue)}

**Token generation (via css-theme-generator):**

From the accent colour above, generate three token files:

| Theme | Generated tokens | Use case | File |
|---|---|---|---|
| Light (default) | bg=white, text=#000, accent=#0078D4, hover=#106ebe, border=#e0e0e0 | Default theme, well-lit environments | tokens-light.css |
| Dark | bg=#1e1e1e, text=#ffffff, accent=#0078D4 (brighter), hover=#1084ff, border=#444 | Evening/field use, reduces eye strain | tokens-dark.css |
| High-contrast | bg=black, text=white, accent=#0078D4 (higher sat), border=white | Accessibility (WCAG AAA), outdoor high-sun | tokens-hc.css |

**Colour accessibility check:**
- Light theme: All text/accent pairs tested against WCAG AA (4.5:1 minimum)
- Dark theme: Same; check reversed contrast (light on dark)
- High-contrast: All pairs checked against WCAG AAA (7:1 minimum)
- Test tool: {WebAIM contrast checker / Stark / other}

**Theme switching:**
- Default: Light (at app startup)
- User preference: Settings → Theme (Light / Dark / High-Contrast) + "Match system" toggle
- System preference: Respect `prefers-color-scheme` media query (on first load)

---

## Typography

**Font family:**
- Primary: Segoe UI (Windows standard; available macOS system fonts, fallback `-apple-system, BlinkMacSystemFont, 'Segoe UI'`)
- Monospace: Consolas (development context only; not in UI)
- Fallback chain: Segoe UI → system sans-serif → sans-serif

**Sizes & weights:**

| Element | Size | Weight | Line-height | Use |
|---|---|---|---|---|
| Heading 1 (H1) | {32px} | {700 (bold)} | {1.2} | Page title, modals |
| Heading 2 (H2) | {24px} | {700} | {1.2} | Section title |
| Heading 3 (H3) | {18px} | {600 (semibold)} | {1.3} | Subsection |
| Body text | {16px} | {400 (regular)} | {1.5} | Paragraphs, descriptions |
| Button text | {16px} | {600 (semibold)} | {1.2} | CTA, form buttons |
| Caption / label | {12px} | {400} | {1.4} | Form labels, helper text, timestamp |
| Monospace | {13px} | {400} | {1.4} | Error messages, codes |

**Text expansion room:** German +15%, French +10% (leave padding in English copy for translation).

---

## Themes (Light / Dark / High-Contrast)

**Light theme (default):**
- Background: White (#ffffff)
- Text: Dark grey (#1f1f1f)
- Accent: {Primary colour, e.g., #0078D4}
- Hover/active: Darker accent (e.g., #106ebe)
- Disabled: Light grey (#cccccc)

**Dark theme:**
- Background: Dark grey (#1e1e1e)
- Text: White (#ffffff)
- Accent: Brighter version of primary (e.g., #0084ff for better readability on dark)
- Hover/active: Even brighter accent
- Disabled: Medium grey (#555555)

**High-contrast theme:**
- Background: Pure black (#000000)
- Text: Pure white (#ffffff)
- Accent: Highly saturated primary (e.g., #0078D4 at 100% sat, no desaturation)
- Borders: White or accent (no grey)
- Disabled: Dark grey (#333333)

**Motion in dark theme:** Subtle (reduced saturation of animations; no flashing).

---

## Density & Component Library

**UI density:** {Comfortable / compact / dense}

| Density | Spacing | Component style | Use case |
|---|---|---|---|
| Comfortable | 16px gutters, 16px padding inside buttons | Generous, spacious | Mobile, new users, accessibility |
| Compact | 8px gutters, 12px padding | Standard, Fluent/Material default | Web, general |
| Dense | 4px gutters, 8px padding | Minimal, data-heavy | Power users, data tables, dashboards |

**Component library:** {E.g., Fluent UI for web, MAUI native for mobile, WinUI for Windows}

**Component library mapping (framework-specific; choose based on platform):**
| Component | {Framework} equivalent | Usage | Notes |
|---|---|---|---|
| Button (primary) | {component} (accent style) | CTA, submit | EXAMPLE - replace with actual component name |
| Button (secondary) | {component} (neutral style) | Cancel, skip | Border, no background |
| Form input | {component} | Text, email, phone | With label, validation error |
| Dropdown | {component} | Select options | Combobox for large lists |
| Table | {component} | Data list | Sortable, paginatable |
| Modal / Dialog | {component} | Confirm actions, forms | Backdrop, close button, focus trap |
| Toast / Alert | {component} | Feedback | 3-sec auto-dismiss |

**Custom components (marked as `custom` in screen inventory):**
- {Custom component name} — {purpose} — {framework-agnostic description}

---

## Iconography

**Icon library:** {Framework-standard icon set — TECH-OPEN:D9}

**Icon sizes:**
| Use | Size | Context |
|---|---|---|
| Navigation tabs | {24px} | Bottom tabs (mobile), top nav (desktop) |
| Button icons | {18px} | Inside buttons, with label (e.g., "← Back") |
| Inline (text-level) | {16px} | Warnings, info, beside text |
| Large cards | {32px} | Hero cards, sections |

**Icon style:** {Outline / filled / custom} — specify per platform.

**Label all icons:** visible label (preferred) or `aria-label` (if icon-only button).

---

## Imagery & Illustration

**Photography style:** Realistic logistics scenes (drivers, vehicles, yards); sourced from Unsplash/Pexels (free, no real people's personal data); professionally shot, diverse representation.

**Illustration:** {None for v1; cost; defer to v2 if budget allows}

**Emoji:** {Not in UI (too casual for logistics); if needed, use for reactions only, not status icons}

---

## Motion & Animation

**Overall motion philosophy:** {Subtle, purposeful; never distracting}

**Transition animations:**
- Page transition: Fade in 200ms (easing `easeInOutQuad`)
- Focus ring: Appear 100ms (no easing)
- Hover state: Colour change 100ms
- Success toast: Fade in 200ms, then auto-dismiss after 3 sec with fade-out 200ms

**Loading indicators:**
- Spinner: Fluent Spinner component, size 24px, primary accent colour
- Progress bar: Fluent ProgressIndicator (indeterminate until %, then determined)

**Micro-interactions:**
- Button press: Subtle colour shift + slight scale (98% scale, 50ms) → feels responsive without distraction
- Form error appearance: Slide down 150ms with red border highlight

**Reduced motion:** Respect `prefers-reduced-motion` media query; disable all animations, show static states instead.

**Haptics (mobile):** Light haptic feedback on button press (feedback 10ms), success buzz (pattern 20–30ms); disable if user has reduced motion set.

---

## Design Deliverables & Approvals

**Deliverable list:**
- Figma design system (web: light + dark + high-contrast; mobile: iOS + Android layout variants; desktop: Windows + macOS)
- Design specs (margins, padding, font sizes, colour values, component spacing) exported as JSON for dev handoff
- Accessibility audit (contrast ratios, focus order, screen-reader labelling) checklist
- Design-to-dev handoff doc (Figma comments, component mapping, special instructions)

**Approval flow:**
- Design team creates mockups in Figma (link shared for feedback)
- PM reviews for alignment with UX brief
- Accessibility review (contrast, focus, labels)
- Stakeholder review + sign-off (Phase 9 mockup show-back)

**Mockup show-back process:**
1. Present mockups for [{Segment}] across devices (web, iOS, Android, Windows, macOS as applicable)
2. Gather reactions: Accept / Change (free text) / Reject / Question
3. Log each reaction as PD-decision (ID, who, status, rationale)
4. Revise only noted changes; re-show sub-set
5. Sign off when decision owner accepts

---

End of UI Design Brief. See `platform-deliverables.md` for platform-specific implementation details.
```

---

## Template 5: platform-deliverables.md

Location: `docs/product/platform-deliverables.md`

Primary consumers: Architect, solution-generator skill, UI/platform developers.

```markdown
# Platform & Deliverables Register

**Status:** Draft / Confirmed  
**Respondents:** {Names}  
**Last updated:** {Date}  
**Open items:** {Unresolved platform decisions}

## Platforms & Surfaces Matrix

### Web (DLV-001)

| Question | Answer |
|---|---|
| **Build web app?** | {Yes / No} |
| **Type** | {SaaS / internal tool / public web / hybrid} |
| **Rendering** | {Server-side / interactive hybrid / static} |
| **Public site** | {Yes / No}; if yes, {CMS / static HTML} |
| **Authenticated app** | {Yes / No}; if yes, persistent session |
| **PWA (installable)** | {Yes / No}; if yes, {offline requirements} |
| **Browsers & versions** | {EXAMPLE - replace with target browsers} |
| **Minimum browser versions** | {EXAMPLE - replace with minimum versions} |
| **SEO needed** | No (internal tool, no public indexing) |
| **Responsive breakpoints** | Mobile (<600px), tablet (600–900px), desktop (>900px) |
| **Performance budget** | FCP <2s, TTI <4s, page <1MB |
| **Feature parity (see cross-surface)** | Route assignment identical across platforms |

**Deliverable:** Web app hosted on {cloud provider}, auto-deployed via CI/CD pipeline.

---

### Mobile — iOS (DLV-002)

| Question | Answer |
|---|---|
| **Build iOS?** | {Yes / No} |
| **Form factor** | {Phone / tablet / both} |
| **Framework** | {Framework — TECH-OPEN:D9} |
| **OS versions** | {EXAMPLE - iOS 16+} |
| **Device features** | {List: GPS / camera / push / other} |
| **Offline-first** | {Yes / No} |
| **Offline sync conflict resolution** | {Strategy: server-wins / client-wins / user-decides} |
| **Native feel vs. shared UI** | {Decision: platform-native / shared code / hybrid} |
| **Store distribution** | {Public App Store / internal / beta track} |
| **Auto-update** | {How updates are delivered} |
| **Code signing** | {Apple Developer certificate / in-house} |
| **Notarisation** | {Required / N/A} |
| **Platform-specific storage** | {iCloud / Keychain / other} |

**Deliverable:** {EXAMPLE - replace with deployment details}.

---

### Mobile — Android (DLV-003)

| Question | Answer |
|---|---|
| **Build Android?** | {Yes / No} |
| **Form factor** | {Phone / tablet / both} |
| **Framework** | {Framework — TECH-OPEN:D9} |
| **OS versions** | {EXAMPLE - Android 11+} |
| **Device features** | {List: GPS / camera / push / other} |
| **Offline-first** | {Yes / No} |
| **Store distribution** | {Google Play Store / direct APK / enterprise track} |
| **Auto-update** | {How updates are delivered} |
| **Code signing** | {Google Play signing / in-house} |
| **Device file access** | {Permissions required} |
| **Managed devices** | {MDM support: yes / no / v1.1+} |

**Deliverable:** {EXAMPLE - replace with deployment details}.

---

### Desktop — Windows (DLV-004)

| Question | Answer |
|---|---|
| **Build Windows?** | {Yes / No} |
| **Framework** | {Framework — TECH-OPEN:D9} |
| **OS versions** | {EXAMPLE - Windows 10 (1909+), Windows 11} |
| **Installer type** | {MSIX / EXE / App Store} |
| **Auto-update** | {How updates are delivered} |
| **Code signing** | {Certificate type / signing strategy} |
| **UAC (Admin rights)** | {Required / not required} |
| **Shell integration** | {Yes / no}; if yes, {context menu / other} |
| **Tray icon** | {Yes / no} |
| **Accessibility** | {VoiceOver / narrator / other} |
| **Remote desktop (RDP)** | {Supported / not supported}; if yes, note limitations |

**Deliverable:** {EXAMPLE - replace with deployment details}.

---

### Desktop — macOS (DLV-005)

| Question | Answer |
|---|---|
| **Build macOS?** | {Yes / No} |
| **Framework** | {Framework — TECH-OPEN:D9} |
| **OS versions** | {EXAMPLE - macOS 11+} |
| **Processor support** | {Intel / Apple Silicon / universal binary} |
| **Installer type** | {DMG / PKG / App Store} |
| **Code signing & notarisation** | {Strategy and timeline} |
| **Auto-update** | {Manual / Sparkle / App Store auto-update} |
| **App store?** | {Yes / no}; if no, note restrictions |
| **Menu bar integration** | {Yes / no} |
| **Platform-specific features** | {iCloud sync / spotlight / other} |
| **Accessibility** | {VoiceOver testing level} |

**Deliverable:** {EXAMPLE - replace with deployment details}.

---

### Cross-Surface Decisions

| Question | Answer |
|---|---|
| **What's identical across all surfaces?** | Core domain logic (route assignment, driver list, sync). Dispatch API, data schema. |
| **What's platform-idiomatic?** | Navigation pattern (web: sidebar, mobile: tabs, desktop: menu bar). Input method (touch on mobile, mouse + keyboard on desktop). Font/density per platform guidelines. |
| **Shared code strategy** | MAUI for mobile + Windows (logic + UI shared). Blazor for web (shared API, separate UI). Minimal duplication; API-first design so any frontend can consume. |
| **One backend or per-surface BFF?** | One backend REST API (v1); no separate BFF; mobile + desktop GET same data, POST same commands. |
| **Account / session continuity** | User signs in once per device (session token stored securely per platform). Sign out is local (not sync across devices). One user can be logged in on web + mobile simultaneously (acceptable for internal tool). |

---

## Feature Parity Table

| Feature / capability | Web | iOS | Android | Windows | macOS | Notes |
|---|---|---|---|---|---|---|
| {Core feature 1} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {EXAMPLE - same, platform-idiomatic, or notes} |
| {Core feature 2} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {Notes} |
| {Desktop-only feature} | {✓ / —} | — | — | {✓ / —} | {✓ / —} | {Desktop-only rationale} |
| {Mobile-only feature} | — | {✓ / —} | {✓ / —} | — | — | {Mobile-only rationale} |
| {Optional feature} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {Notes} |
| {Platform-specific feature} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {✓ / —} | {Native implementation details per platform} |

---

## Deliverables Register (DLV-nnn)

Complete list of shipping artifacts per platform and release phase:

| DLV ID | Deliverable | Platform(s) | Owner | Acceptance criterion | Release phase | Status |
|---|---|---|---|---|---|---|
| DLV-001 | {Web app} | {Web} | {EXAMPLE - replace with owner} | {EXAMPLE - core features work, performance targets met, WCAG AA} | {v1.0} | {In progress / Done / Deferred} |
| DLV-002 | {iOS app} | {iOS phone + tablet} | {EXAMPLE - replace with owner} | {EXAMPLE - target OS version, offline-capable, key features functional} | {v1.0} | {Status} |
| DLV-003 | {Android app} | {Android phone + tablet} | {EXAMPLE - replace with owner} | {EXAMPLE - target OS version, Play Store listing} | {v1.0} | {Status} |
| DLV-004 | {Desktop app (Windows)} | {Windows} | {EXAMPLE - replace with owner} | {EXAMPLE - installer type, auto-update functional} | {v1.1} | {Status} |
| DLV-005 | {Desktop app (macOS)} | {macOS} | {EXAMPLE - replace with owner} | {EXAMPLE - installer type, universal binary} | {v1.1} | {Status} |
| {DLV-nnn} | {Deliverable type} | {Platform(s)} | {Owner} | {Acceptance criterion} | {Release phase} | {Status} |
| {DLV-nnn} | {API documentation} | {Web} | {Owner} | {OpenAPI spec, documentation complete} | {v1.0} | {Status} |
| {DLV-nnn} | {Prototype} | {HTML (local)} | {EXAMPLE - designer + developer} | {All top journeys testable, states functional} | {Phase 11} | {Status} |

---

## Distribution & Update Channels

| Platform | Distribution | Update mechanism | Version tracking | Rollback |
|---|---|---|---|---|
| Web | {EXAMPLE - cloud host, auto-deployed} | {Server-side / client-side} | {Semantic versioning} | {Previous version strategy} |
| iOS | {App Store / TestFlight / enterprise} | {App Store auto-update or manual} | {App Store version, in-app version} | {App Store archive limit noted} |
| Android | {Google Play / direct APK / enterprise} | {Play Store auto-update or manual} | {Google Play version code} | {APK archive strategy} |
| Windows | {Windows Store / company portal / direct} | {MSIX auto-update or manual} | {Package version} | {Previous version archive} |
| macOS | {App Store / company portal / direct} | {Manual or auto-update framework} | {App version in About} | {Archive strategy} |

---

End of Platform & Deliverables. See `discovery-decisions.md` for decision log.
```

---

## Template 6: discovery-decisions.md

Location: `docs/product/discovery-decisions.md`

Live log of all decisions captured during the interview. Updated in real-time as each phase concludes.

```markdown
# Product Discovery — Decision Log

**Status:** Draft (interview in progress) / Confirmed  
**Respondents:** {Names, roles}  
**Last updated:** {Date}  
**Interview dates:** {Start date} – {Current date}

## Format

| PD ID | Phase | Decision / Finding | Who | Status | Flag | Rationale / Notes |
|---|---|---|---|---|---|---|
| PD-001 | 0 | Respondent mode: {Mode} | {Name} | Resolved | | {Rationale} |
| PD-002 | 1 | Problem statement | {Name} | Resolved | | {Evidence source, validation method} |
| PD-003 | 2 | Primary audience segment | {Name} | Assumption | | {What is known vs. guessed; validation method if assumption} |
| ... | ... | {Further decisions per phase} | ... | Resolved / Assumption / Deferred / Conflict / N/A | TECH-OPEN:D{n} or blank | ... |
| PD-nnn | 16 | Open assumption: {Topic} | {Owner} | Assumption | | Validation method: {method}; target date {date} |
| PD-nnn | 17 | {Technical question} | {Role} | Deferred | TECH-OPEN:D{n} | Flagged for design-interrogation Dimension {n}; no customer-facing impact in v1 |

---

## Summary

**Total decisions:** 40  
**Resolved:** 32  
**Assumption:** 5 (to validate in beta or post-launch)  
**Deferred:** 3 (decided later; owners named, dates set)  
**Conflict:** 0  
**N/A:** 0

**Open items (not yet resolved):**
- Legal docs (T&Cs, privacy): awaiting legal team draft (due 30 Jun 2027)
- Desktop platforms (Windows, macOS): deferred to v1.1 decision

---

End of Decision Log.
```

---

## Template 7: prototype/walkthrough.md

Location: `docs/product/prototype/walkthrough.md`

Script for Phase 11 clickable-prototype validation round.

```markdown
# Prototype Walkthrough Script

**Product:** {Product Name}  
**Date:** {Date}  
**Participants:** {Name, role}; {Name, role}; facilitator: {Name}  
**Prototype version:** {Version, e.g., "v1.0-RC1"}  
**Prototype link:** {Local path or private Artifact URL}  
**Duration:** ~30 minutes  
**Recording:** {Yes / No}

---

## Briefing (2 min)

"We've built a clickable prototype of the core journeys. It's not the final product — it's interactive wireframes and mockups to test our understanding. Ignore any placeholder data or unpolished UI; focus on the flow and whether it matches what you envisioned. Think aloud: if something confuses you, say so. No wrong answers."

**Prototype note:** *[Visible label on every screen]* "PROTOTYPE — not the product. Local demo; no real data or services."

---

## Task 1: Assign a Route (5 min)

**Scenario:** "It's 6 AM. You log in and see today's tasks. You need to assign Alice and Bob to the 10 AM zone-A route and the 12 PM zone-B route."

**Task steps:**
1. Open the prototype (home screen)
2. Log in (use demo credentials if prompted; if not, proceed to dashboard)
3. Find the route board / dashboard
4. Locate 10 AM zone-A route
5. Assign Alice to zone-A route
6. Assign Bob to zone-B route
7. Confirm / send the assignments

**Success criterion:** Assignments sent; both drivers see routes in their app within 30 seconds (simulate with a "click to refresh" or auto-update screen).

**Observations:**
- Where did the user look first? (Expected: dashboard/board)
- Did they find the routes easily? (Expected: route cards visible)
- Did they understand how to assign (expected: drag-drop or select + assign button)?
- Any confusion about zone labels or route details?
- Did they expect any feedback after clicking "Send"? (Expected: success toast)

---

## Task 2: Confirm a Delivery (3 min)

**Scenario:** "You're Bob, a driver. You've completed the first delivery stop. Confirm it and move to the next task."

**Task steps:**
1. Switch to driver view (button / theme toggle on prototype, if available)
2. Find the task list / current route
3. Open the first delivery task
4. Take a photo (simulated; click "camera" button or skip)
5. Confirm / mark delivery complete
6. Proceed to next task

**Success criterion:** Delivery marked complete; next task appears. Driver list updated (show "on task 2").

**Observations:**
- Did the user understand they were switching to driver view?
- Was the task list clear (current task highlighted)?
- Did they expect a photo upload step? (If yes and we didn't have it, note as feedback.)
- Any confusion about the next-task flow?

---

## Task 3: View Daily Report (2 min)

**Scenario:** "It's 4 PM. You want to see today's summary: how many routes completed, any exceptions."

**Task steps:**
1. Navigate to Reports or Dashboard
2. Find today's daily summary
3. Identify: total routes, completed routes, exceptions (if any)

**Success criterion:** User finds report; can answer: "How many routes completed today?" and "Any exceptions?"

**Observations:**
- Did the user navigate to the right place? (Expected: Reports / Dashboard tab)
- Was the summary clear and scannable?
- Did they expect drill-down details (click a completed route to see details)? If yes, did they find the link?
- Is the data presentation (tables, cards, numbers) easy to understand?

---

## Task 4: Go Offline and Sync Back (3 min)

**Scenario:** "You're a driver in a warehouse (underground, no signal). You assign yourself to a new zone using the app. Then you leave the warehouse and regain signal. Watch what happens."

**Task steps:**
1. Enable offline mode (if prototype has a toggle; explain if not: "imagine you're offline")
2. Make a change (e.g., reassign yourself to a different task or zone)
3. Toggle offline OFF to re-online
4. Observe sync behaviour

**Success criterion:** Offline changes are preserved; no data loss; sync completes without error (or shows a clear retry if conflict).

**Observations:**
- Did the user expect to see an offline indicator? (Current design: badge "Offline", button to retry sync)
- Did they understand that changes are saved locally and sync'd when online?
- Any surprise about the sync result?
- If a conflict appeared, was the resolution clear (server wins, show user the new data, ask them to re-enter if they want to override)?

---

## Task 5: Handle an Exception (2 min)

**Scenario:** "You're trying to sync but the app shows 'Can't sync right now. Retrying every 10 seconds.' What do you do?"

**Task steps:**
1. Observe the error state (modal or banner showing sync failure)
2. Click "Retry" (or wait for auto-retry)
3. Observe recovery (should retry and eventually succeed, or show persistent error)

**Success criterion:** User understands the error is temporary (not permanent); they're not blocked (can keep working offline).

**Observations:**
- Was the error message clear and reassuring?
- Did they try to click Retry? (Expected: obvious button)
- Did they expect more information (e.g., "Check your internet connection")? If yes, note as UX improvement.
- Confidence that the app will auto-recover? (Expected: yes)

---

## Reactions & Feedback (5 min)

After all tasks, ask the respondent:

### Q1: Overall Reaction
**"Overall, does this prototype match what you envisioned? Accept, change something, reject, or questions?"**

**Options:**
- *Accept* → "Let's move forward with this design."
- *Change* → "What would you change?" (free text, capture 3–5 main changes)
- *Reject* → "What's missing or wrong?" (free text, note for major redesign)
- *Question* → "What's unclear?" (free text, note for Phase 12 technical decisions)

### Q2: Specific Areas
**"Any specific screens or flows you'd change?"**

Listen for:
- Terminology confusion (are field names clear?)
- Missing features (did they expect something?)
- Flow changes (different order of steps)
- Performance concerns (is it fast enough?)

### Q3: Confidence
**"How confident are you that the team can build this in 6 months with 5 people?"**

- 1 (not confident, too complex) to 10 (confident, straightforward)
- If <6, ask: "What's the risk? What would make you more confident?"

---

## Observations & Next Steps

**Facilitator notes:**
- [Task 1 observation: User expected route cards to show driver names, not zones. Design change: label route cards by destination/zone + key driver count.]
- [Task 2 observation: User looked for "Complete" button immediately; found it without issue.]
- [Task 3 observation: User expected a "daily vs. weekly vs. monthly" report toggle; we don't have it in the prototype. Decide v1.1.]
- [Task 4 observation: Offline mode toggle is not obvious; add a UI indicator on mock-up.]
- [Task 5 observation: Error message is good; user felt reassured.]

**Design changes logged as PD-decisions (from show-back reactions):**
- {PD-nnn (Task feedback)}: {Description of change}. Status: {Resolved / Change / Reject}. Owner: {Role}. Revision: {Action}.

**Sign-off:**
- [ ] All tasks completable by representative from each audience segment (dispatch manager, driver, admin)?
- [ ] No dead screens or broken navigation?
- [ ] Offline mode + sync conflict handling clear to users?
- [ ] Error states (sync fail, not found, no permission) all present and clear?

---

End of Walkthrough Script.
```

---

## Template 8: prototype/validation-log.md

Location: `docs/product/prototype/validation-log.md`

Results of the Phase 11 walkthrough and any follow-up validation (beta testing, user testing, QA).

```markdown
# Prototype Validation Log

**Product:** {Product Name}  
**Prototype version:** {Version}  
**Validation date:** {Date}  
**Participants:** {Names, roles}  
**Facilitator:** {Name}  
**Notes:** {Any context, e.g., "Remote session via Zoom"}

---

## Validation Results

| Task # | Task name | Persona | Result | Observations | PD change | Status |
|---|---|---|---|---|---|---|
| 1 | {Task name} | {Persona} | Succeeded | {Observations: what worked well, any confusion, unexpected expectations} | {PD-nnn reference or —} | {Resolved / Change requested / Deferred} |
| 2 | {Task name} | {Persona} | Succeeded | {Observations} | {PD-nnn reference or —} | {Status} |
| 3 | {Task name} | {Persona} | Struggled | {Observations: where user got stuck, what they expected, suggestions} | {PD-nnn reference} | {Change requested / Deferred} |
| 4 | {Task name} | {Persona} | Succeeded | {Observations} | {PD-nnn reference or —} | {Status} |
| 5 | {Task name} | {Persona} | Succeeded | {Observations} | {PD-nnn reference or —} | {Status} |
| Overall prototype sign-off | — | {Personas} | Succeeded / Struggled / Failed | {Overall reaction to prototype} | {PD-nnn list} | {Accept / Change / Reject} |

---

## Summary of Findings

**Total tasks:** 5  
**Succeeded:** 4  
**Struggled:** 1  
**Failed:** 0

**Key observations:**
1. {PD-nnn reference: {Observation about design or interaction}}
2. {PD-nnn reference: {Observation}}
3. {Observation: {Topic covered}; {Confidence or next steps}}
4. {Observation: {Topic covered}; {Confidence or next steps}}

---

## Unresolved Findings / Questions

| Question | Owner | Target date | Notes |
|---|---|---|---|
| {EXAMPLE - deferred design question} | {Owner} | {design-interrogation Dimension n} | {Why deferred, acceptance criteria} |
| {EXAMPLE - deferred technical question} | {Owner} | {design-interrogation Dimension n} | {Why deferred, acceptance criteria} |

---

## Prototype Defects & Polish

| Defect | Severity | Status |
|---|---|---|
| {EXAMPLE - description of usability issue} | {High / Medium / Low} | {Fixed / Deferred / Wontfix} |
| {EXAMPLE - description of accessibility issue} | {High / Medium / Low} | {Status} |
| {EXAMPLE - description of polish issue} | {High / Medium / Low} | {Status} |

---

## Design Decision Sign-Off

**All prototype feedback reviewed and approved by:** {Decision owner name}

**Date:** {Date}

**Next step:** {Describe changes to prototype and hand-off readiness}. Prototype is approved for hand-off to build team.

---

End of Validation Log.
```

---

## Confidentiality Note (Include in all documents)

**Confidentiality:** This document contains commercial information including product strategy, pricing, roadmap, and user research. It is intended for team members and trusted stakeholders. Do not share publicly without explicit approval. Check repository visibility before committing to version control.

**Personas:** All personas are fictional composites based on research, not real people. No personally identifiable information is included.

---

## Notes for the Skill

1. **Real-time logging:** As each phase concludes, the skill appends the PD-decisions to `discovery-decisions.md` immediately (progressive capture). This allows resumable sessions — on restart, the skill checks what's already logged and offers to continue from there.

2. **Show-back reactions:** Reactions gathered during mockup and prototype show-backs (Accept / Change / Reject / Question) are logged as PD-decisions with status (Resolved / Change / Reject / Question) and rationale.

3. **Template population:** The skill reads these templates and populates placeholders `{...}` with actual values from each phase. Documents are created / updated in `docs/product/` as the interview progresses.

4. **Audience → design mapping:** The traceability table in `audience-profile.md` is referenced by `ux-brief.md` and `ui-design-brief.md` so designers know which audience constraints drive each UX/UI decision.

5. **Screen inventory:** Every screen designed in the prototype gets an `SCR-nnn` ID. The `screen-inventory` table in `ux-brief.md` lists all screens, their purpose, audiences, states, components, and mapping to journeys and PD-decisions.

6. **DLV register:** Every deliverable (web app, iOS, documentation, etc.) gets a `DLV-nnn` ID with owner, acceptance criterion, release phase, and status. This register lives in `platform-deliverables.md` and informs `design-interrogation` Phase 0 (A5 — surfaces & deliverables).

7. **Format consistency:** All documents use:
   - Markdown (GitHub-flavoured for tables)
   - Status header (Draft / Confirmed)
   - Respondents list
   - Open items section
   - Section headings (##, ###)
   - Tables for structured data
   - Avoid a lone `---` line at the top of the file (reserved for YAML frontmatter); use `---` freely as section separators within content

---

End of Output Templates.
