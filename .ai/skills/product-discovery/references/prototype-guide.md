# Prototype Guide: Wireframes, Mockups, and Clickable Prototypes

How to produce and validate wireframes, mockups, and a clickable prototype from the product-discovery scaffold during the interview.

## Overview

Prototypes evolve through three fidelity levels during the interview, each with its own show-back round:

| Level | Fidelity | When | Purpose | Format |
|-------|----------|------|---------|--------|
| **Wireframe** | Low (greyscale, structure only) | End of Phase 8 (UX) | Validate IA, navigation, flows, content hierarchy | `docs/product/prototype/wireframes/index.html` |
| **Mockup** | High (tokens, real type, content) | End of Phase 9 (UI) | Validate look & feel, tone, density, brand fit | `docs/product/prototype/mockups/` (per screen × surface) |
| **Clickable Prototype** | Interactive (working nav, forms, states, toggles) | Phase 11 | Walkthrough, validation, and hand-off to design/build | `docs/product/prototype/index.html` |

## Folder Structure

Place all prototype assets under `docs/product/prototype/`. The shared scaffold provides the core HTML/CSS/JS shell; wireframe, mockup, and clickable prototype modes are toggled via a body class without requiring separate folder hierarchies:

```
docs/product/
├── prototype/
│   ├── index.html                    # Shared prototype shell (switchable between wireframe/mockup/clickable modes)
│   ├── prototype.css                 # Shared styling (device frames, state toggles, responsive layout)
│   ├── prototype.js                  # Shared interactivity (navigation, theme/language/state toggles)
│   ├── tokens.css                    # Generated tokens (light, dark, high-contrast themes)
│   ├── SCR-001.html                  # Individual screen definitions (optional; can also be embedded in index.html)
│   ├── SCR-002.html
│   ├── ...
│   ├── walkthrough.md                # Task-based walkthrough script (Phase 11)
│   ├── validation-log.md             # Results of walkthrough and validation
│   └── README.md                     # Build and handoff instructions
│
├── discovery-decisions.md            # Consolidated log (PD-nnn) — includes prototype reactions from all fidelity levels
└── ...other discovery documents...
```

**Wireframe, mockup, and clickable modes:** The shared scaffold uses a data-fidelity attribute or body class (e.g., `body.wireframe-mode`) to switch the token palette to greyscale for wireframes. Mockups and the clickable prototype use the same scaffold with different token values and interactivity levels.

## Wireframe Level

Low-fidelity, structure-focused; greyscale to avoid design decisions in this phase.

### When to Produce

End of Phase 8 (UX), after journeys, IA, navigation, and screen layout are resolved. Do not wait for visual design (Phase 9).

### What to Include

- **Top journeys only**: 3–5 key user flows (e.g., sign-in, create item, list view).
- **Real layout**: Accurate information hierarchy, spacing, and text flow — not Lorem Ipsum.
- **Placeholder content**: Realistic persona-based sample data in the product's language; no real personal data.
- **State templates**: One key screen in multiple states (empty, loading, error, offline).
- **Greyscale only**: Apply the `wireframe-mode` body class in `tokens.css` to neutralise color tokens. Convey structure, not aesthetics.

Example wireframe screen:

```html
<section class="screen" id="SCR-001" data-label="Dashboard">
  <div class="device-frame">
    <div class="device-frame-header">Dashboard</div>
    <div class="device-frame-content">
      <h1>Welcome, Maria</h1>
      <p>Overview of your recent activity.</p>
      <div class="card">
        <h3>Task 1: Review Invoice #2024-001</h3>
        <p>Amount: $1,200 | Due: Tomorrow</p>
        <button>Open</button>
      </div>
      <!-- More cards... -->
    </div>
  </div>
</section>
```

### Using Wireframe Mode

The scaffold includes a `body.wireframe-mode` class in `tokens.css` that neutralises all colour tokens to greyscale. Enable wireframe mode by toggling the class on `<body>`:

```css
/* tokens.css: Wireframe Mode - Neutral Greyscale */
body.wireframe-mode {
  --b-bg: #ffffff;
  --b-surface: #f5f5f5;
  --b-surface-2: #e8e8e8;
  --b-surface-3: #d9d9d9;
  --b-border: #999999;
  --b-text: #333333;
  --b-text-2: #666666;
  --b-text-3: #999999;
  --b-accent: #666666;
  --b-accent-dim: #cccccc;
  --b-success: #666666;
  --b-warning: #999999;
  --b-danger: #666666;
}
```

In the prototype shell (`index.html`), add a toolbar toggle to switch wireframe mode on/off, or set it at startup:

```html
<body class="theme-light wireframe-mode">
  <!-- Wireframes visible in greyscale -->
</body>
```

For mockup and clickable prototype modes, remove the `wireframe-mode` class so the full token palette (with the accent colour) is visible.

### Show-Back Round (Wireframe)

After wireframes are built:

1. **Present**: Show each wireframe on the respondent's device, walk through one journey end-to-end.
2. **Task-based reactions**: Ask "Can you find [feature]?" or "What would you do here?" — don't ask "Do you like it?"
3. **Log reactions** as `PD-nnn` decisions:
   - *Accepted* — structure is correct, move forward.
   - *Change* — describe what needs to change (scope, flow, labels).
   - *Reject* — fundamental issue; rework this screen.
   - *Question* — unclear intent; clarify before moving on.
4. **Revise** only what was rejected or flagged for change.
5. **Re-show** the revised screens to confirm.
6. **Record** decisions in `discovery-decisions.md`:
   ```
   **PD-041** — Dashboard wireframe structure
   Status: Resolved
   Who: Product Owner
   Decision: Accepted with one change — move the "Task summary" card above the "Recent activity" list.
   Rationale: Users want an overview first, then details.
   ```

## Mockup Level

High-fidelity, brand-aligned; uses generated tokens and realistic typography.

### When to Produce

End of Phase 9 (UI), after visual design, tokens, and typography are confirmed. Build on the approved wireframes.

### What to Include

- **Per-surface variants**: Web, iOS, Android, Windows, macOS — with platform-idiomatic chrome (header, navigation).
- **Generated tokens**: Accent color → theme-generator → tokens.css. Mockups consume the same tokens as the final product.
- **Real typography**: Font family, size, weight, line-height per the design brief.
- **Theme variants**: Light, dark, and high-contrast mockups of at least one key screen.
- **State variants**: One screen (e.g., list) in default, empty, loading, error, offline, success states.
- **Realistic content**: Persona-based sample data, product language, no lorem ipsum, no real PII.
- **Audience annotations**: Note which audience findings constrain each mockup (e.g., "Large type for 65+ users").

Example mockup:

```html
<section class="screen" id="SCR-001-web" data-label="Dashboard (Web)">
  <div class="device-frame" style="max-width: 1024px;">
    <div class="device-frame-header">Dashboard</div>
    <div class="device-frame-content">
      <!-- Token-driven styling -->
      <h1 style="color: var(--b-text); font-size: 24px;">
        Welcome, Maria
      </h1>
      <p style="color: var(--b-text-2);">
        Overview of your recent activity.
      </p>
      <!-- Components use tokens -->
      <div class="card" style="background-color: var(--b-surface); border-color: var(--b-border);">
        <h3 style="color: var(--b-text);">Task 1: Review Invoice #2024-001</h3>
        <p style="color: var(--b-text-2);">Amount: $1,200 | Due: Tomorrow</p>
        <button style="background-color: var(--b-accent); color: white;">Open</button>
      </div>
    </div>
  </div>
</section>
```

### Feeding Tokens

1. **Generate tokens** from the accent colour:
   - For **web mockups**: Use `css-theme-generator` skill → produces `tokens.css` with `--color-primary-50..950` scale tokens (light, dark, high-contrast).
   - For **native app mockups** (MAUI, WinUI, etc.): Use `xaml-theme-generator` → produces platform-specific color resources. High-contrast theme is always included in scaffold or generators; do not duplicate.
   - For **platform-specific refinement**: Check [`.ai/skills/xaml-theme-generator/SKILL.md`](../xaml-theme-generator/SKILL.md) for output format (Resources/Styles/Colors.xaml for MAUI, App.xaml for WinUI/UWP).

2. **APPEND generated tokens to the scaffold** in `docs/product/prototype/tokens.css`:
   - Keep the scaffold's existing `--b-accent`, `--b-bg`, `--b-text` definitions as fallbacks.
   - APPEND the generated `--color-primary-50..950` scale below them.
   - Define `--b-accent` as an alias from the generated scale:
   ```css
   :root {
     /* Scaffold defaults (fallbacks) */
     --b-accent: #0078d4;
     --b-bg: #ffffff;
     --b-text: #1a1a1a;
     /* ... rest of scaffold defaults ... */

     /* APPEND generated theme tokens */
     --color-primary-50: #f0f8ff;
     --color-primary-100: #e1f0ff;
     /* ... through 950 ... */
   }
   
   /* Override scaffold names with generated scale */
   body.theme-light {
     --b-accent: var(--color-primary-600, #0078d4);
     --b-accent-dim: var(--color-primary-200, #b4d7f1);
   }
   ```

3. **Link in mockups and prototype**:
   ```html
   <link rel="stylesheet" href="tokens.css">
   ```

4. **Update during the interview** if the accent colour changes (Phase 9):
   - Regenerate the `--color-primary-*` scale.
   - APPEND to tokens.css (do not overwrite scaffold fallbacks).
   - Refresh mockup and prototype previews.
   - Re-run contrast check (minimum 4.5:1 for AA, 7:1 for AAA).

### Show-Back Round (Mockup)

After mockups are built:

1. **Present**: Show mockups of 2–3 key screens on actual devices (phone, tablet, desktop).
2. **Fixed reaction set**:
   - *Accept* — look & feel is right, move forward.
   - *Change* — describe what to adjust (spacing, colour, tone, density).
   - *Reject* — start over on this screen.
   - *Question* — clarify before proceeding.
3. **Log reactions** as `PD-nnn` decisions (per screen × surface).
4. **Revise** and re-show.
5. **Record**:
   ```
   **PD-052** — Dashboard mockup (web + mobile variants)
   Status: Resolved
   Who: Design Lead
   Decision: Accept web mockup; change mobile variant to stack the "Task summary" vertically.
   Rationale: On small screens, horizontal layout crowds the content.
   ```

## Clickable Prototype

Interactive, wired-up version that respondents walk through; becomes a hand-off artifact to design and build teams.

### When to Produce

Phase 11 (after UX and UI are confirmed). Assemble from approved wireframes/mockups.

### What to Include

- **Working navigation**: All links navigate to the correct screen.
- **Forms with validation**: Submit buttons respond; show sample validation messages.
- **State toggles**: Toolbar switches for theme, language, state, persona, device frame.
- **Task-based journeys**: Users can complete the top 5–8 workflows end-to-end.
- **Screen-state templates**: Toggle between default, empty, loading, error, offline, success, no-permission for each screen.
- **Accessible from the file system**: No server, no network calls, no external dependencies. Open `index.html` in a browser and run locally.
- **All three fidelities visible**: Wireframe, mockup, and prototype are all available; respondents can compare.

### Building from the Scaffold

1. **Copy the scaffold** to `docs/product/prototype/`:
   
   **POSIX (bash/zsh):**
   ```bash
   cp -r .ai/skills/product-discovery/assets/prototype-scaffold/* docs/product/prototype/
   ```
   
   **PowerShell (Windows):**
   ```powershell
   Copy-Item -Path ".ai/skills/product-discovery/assets/prototype-scaffold/*" -Destination "docs/product/prototype/" -Recurse
   ```

2. **Customize screens**:
   - Edit `index.html` to add your product's screens.
   - Each screen is a `<section class="screen" id="SCR-nnn">`.
   - Use the three example screens (SCR-001 sign-in, SCR-002 list, SCR-003 detail form) as templates.

3. **Update tokens**:
   - Replace `tokens.css` with the version generated from your accent colour.
   - Verify contrast against your WCAG level (AA default).

4. **Add walkthrough tasks**:
   - Create `docs/product/prototype/walkthrough.md` (see **Walkthrough Script** below).

5. **Test locally**:
   - Open `file:///path/to/docs/product/prototype/index.html` in a browser.
   - Test on actual devices (phone, tablet).
   - Verify all links work, all states toggle, all forms respond.

### Screen Inventory

Document each screen in the sidebar and in `ux-brief.md`. Fields:

| Field | Example |
|-------|---------|
| **Screen ID** | `SCR-001` |
| **Screen Name** | Sign In |
| **Purpose** | Authenticate users before accessing the dashboard. |
| **Primary Persona** | Maria (Admin) |
| **Journey** | Authentication → Dashboard |
| **States** | default, loading, error, success, offline |
| **Components** | Form (email + password), Button (Sign In), Link (Create account) |
| **Custom Components** | {None / list custom components if any} |
| **Design Decisions** | {PD-nnn list from show-back rounds} |

### Walkthrough Script

Create `docs/product/prototype/walkthrough.md` with 5–8 task-based scenarios derived from your top journeys. See **Template 7** in [output-templates.md](output-templates.md#template-7-prototypewalkthrough-md) for the canonical format and example structure. The walkthrough defines success criteria and collects reactions (Succeeded / Struggled / Failed) from respondents.


## Show-Back Round Procedure

After each fidelity level (wireframe, mockup, prototype), run a show-back:

### Setup
1. **Prepare**: Have the prototype open on the respondent's device or screen-shared.
2. **Brief**: "I'll walk you through a few tasks. Tell me if anything is confusing or if you'd change something."
3. **No leading questions**: Avoid "Do you like this?" Ask task-based: "Can you find X?" or "What would you do here?"

### During
1. **Observe**: Watch where the respondent clicks, pauses, or looks confused.
2. **Listen**: Record verbatim quotes about what works and what doesn't.
3. **Task-based reactions**: Use fixed options — *Accept / Change / Reject / Question*.
4. **Encourage honesty**: "This is a sketch, not the product. Your feedback shapes the design."

### After
1. **Log decisions**: Record each reaction as a `PD-nnn` decision in `discovery-decisions.md`.
2. **Prioritise changes**: Group by impact (must-change, nice-to-have, defer to later phases).
3. **Revise**: Implement must-changes only; defer the rest.
4. **Re-show**: Share revised screens; confirm the respondent is satisfied before moving on.

## Rules

### Content
- **Realistic personas**: Use fictional composite personas, never real people or real personal data.
- **Product language**: Use the product's actual language(s), not Lorem Ipsum.
- **Sample data**: Consistent with audience and use case (e.g., Maria's invoice amount reflects her typical workload).
- **No real credentials**: Use obvious fakes (`user@example.com`, sample password).
- **No network calls**: All data is static or dynamically generated in JavaScript.

### Scope
- **Built from existing components only**: Mocks use only components available in the chosen UI library (framework-specific components). Mark any custom or placeholder component with a `custom` flag in the screen inventory.
- **No speculative design**: If a component doesn't exist, use the closest available alternative and flag it.
- **Prototype label**: Visible "Prototype — not the product" banner on every screen.

### Handover
- **Private Artifact**: Only publish the prototype as a private Artifact (Claude Docs or similar) if the user explicitly asks. Never share publicly without permission.
- **File system compatible**: Ensure it opens and runs from `file://` with no server, no build step, no external services.
- **Design handoff**: Hand over the prototype, `ux-brief.md`, `ui-design-brief.md`, and `discovery-decisions.md` to the designer and build teams. The prototype is the visual specification.

## Verification Checklist (ui-tester)

Run before sign-off:

- [ ] **Navigation**: All links work; no dead screens. Each link goes to the correct `SCR-nnn`.
- [ ] **Journeys**: Each top workflow (sign-in → dashboard, create item, etc.) is completable end-to-end.
- [ ] **State toggles**: Theme, language, state, persona, device toggles all render correctly and persist during navigation.
- [ ] **Contrast**: Every text/background pair meets the agreed WCAG level (AA default: 4.5:1 for normal text; 3:1 for large text). Test in light, dark, and high-contrast modes.
- [ ] **Keyboard**: Tab order is logical; all interactive elements are focusable; focus indicator is visible (minimum 2px outline).
- [ ] **Screen reader**: State changes announce; form labels are associated; links have meaningful text (not "click here").
- [ ] **Touch targets**: All buttons, links, and form inputs are ≥44×44 pixels.
- [ ] **Reduced motion**: Animations and transitions are disabled when `prefers-reduced-motion: reduce` is set.
- [ ] **Offline/file system**: Prototype opens and functions from `file://` with no server, no network requests, no external CDN.
- [ ] **Responsive**: Layout adapts correctly across device frames (web mobile/tablet/desktop, iOS, Android, Windows, macOS).

## Example: Building a Prototype from Scratch

### Step 1: Copy the scaffold

**POSIX (bash/zsh):**
```bash
mkdir -p docs/product/prototype
cp -r .ai/skills/product-discovery/assets/prototype-scaffold/* docs/product/prototype/
```

**PowerShell (Windows):**
```powershell
New-Item -ItemType Directory -Path "docs/product/prototype" -Force
Copy-Item -Path ".ai/skills/product-discovery/assets/prototype-scaffold/*" -Destination "docs/product/prototype/" -Recurse
```

### Step 2: Define your screens
Edit `docs/product/prototype/index.html`:
```html
<section class="screen" id="SCR-001" data-label="Dashboard">
  <div class="device-frame">
    <div class="device-frame-header">Dashboard</div>
    <div class="device-frame-content">
      <h2>Welcome, Maria</h2>
      <!-- Your content -->
    </div>
  </div>
</section>
```

### Step 3: Update tokens
1. Run the theme generator on your accent colour (e.g., `#0078d4`).
2. APPEND the generated `--color-primary-*` tokens to `tokens.css` `:root` section (do NOT replace the file).
3. Verify contrast in your WCAG level.

### Step 4: Write the walkthrough script
Create `docs/product/prototype/walkthrough.md` with 5–8 tasks.

### Step 5: Test locally

**macOS (open command):**
```bash
open docs/product/prototype/index.html
```

**Windows (PowerShell):**
```powershell
Start-Process "docs/product/prototype/index.html"
```

**All platforms (file URL):**
```
file:///path/to/docs/product/prototype/index.html
```
(Paste the local file path in your browser's address bar.)

### Step 6: Validate
- [ ] All screens navigate.
- [ ] States toggle correctly.
- [ ] Contrast passes WCAG AA.
- [ ] Keyboard navigation works.
- [ ] Runs offline from file system.

### Step 7: Show-back
Present to stakeholders, collect feedback, log `PD-nnn` decisions, revise, and re-show.

## Handing Off to Design and Build

After the prototype is signed off:

1. **ux-brief.md**: Copy screen inventory to `ux-brief.md` with component lists and states.
2. **ui-design-brief.md**: Include the approved token set, typography, and design system reference.
3. **prototype/**: Deliver the entire `docs/product/prototype/` folder as-is; the prototype is the source of truth for layout and interaction.
4. **discovery-decisions.md**: Hand off the log so design and build teams understand the why behind each decision.
5. **validation-log.md**: Include to show where the design was tested and what was learned.

The build team uses the prototype to verify that their implementation matches the approved design.
