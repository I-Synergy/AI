# Prototype Scaffold

A minimal, dependency-free HTML/CSS/JavaScript prototype shell for wireframes, mockups, and clickable demos. Runs directly from the file system with no build step, server, or external dependencies.

## Features

- **Hash-based screen router** — navigate between screens via `#SCR-001` URL fragments
- **Device frame switcher** — preview across web (mobile/tablet/desktop), iOS, Android, tablet, Windows, and macOS layouts
- **Theme toggles** — light, dark, and high-contrast modes with CSS custom properties
- **Language/RTL support** — switch language and right-to-left direction via HTML `dir` attribute
- **Screen state templates** — default, empty, loading, error, offline, success, no-permission states
- **Persona/role switcher** — test different user types (user, admin, guest)
- **Screen inventory sidebar** — quick navigation to all screens
- **Persistent prototype banner** — reminds viewers this is not the product
- **Keyboard accessible** — focus order, visible focus indicators, 44px touch targets, respects `prefers-reduced-motion`
- **Contrast-safe tokens** — CSS variables for brand colors, light/dark variants, high-contrast fallbacks

## Quick Start

1. Open `index.html` directly in a browser (no server needed).
2. Use the toolbar to switch themes, languages, states, personas, and device frames.
3. Click screen links in the sidebar or use the hash (`#SCR-001`, `#SCR-002`, etc.) to navigate.

## File Structure

```
prototype-scaffold/
├── index.html          # Main entry point
├── prototype.css       # Core styling
├── prototype.js        # Router, state management, i18n
├── tokens.css          # Design tokens (light/dark/HC variants)
├── screens/            # (Optional) Separate screen files
└── README.md           # This file
```

## Tokens

Edit `tokens.css` to customize colors. The scaffold provides CSS custom properties:

```css
--b-bg            /* Background */
--b-surface       /* Surface/card background */
--b-surface-2     /* Secondary surface */
--b-surface-3     /* Tertiary surface */
--b-border        /* Border color */
--b-text          /* Primary text */
--b-text-2        /* Secondary text */
--b-text-3        /* Tertiary text */
--b-accent        /* Brand/accent color */
--b-accent-dim    /* Dimmed accent (e.g., hover) */
--b-success       /* Success state */
--b-warning       /* Warning state */
--b-danger        /* Error/danger state */
--b-sidebar-bg    /* Sidebar background */
--b-sidebar-w     /* Sidebar width */
--b-header-h      /* Header height */
```

### Theme Variants

- **Light** (default): `--b-bg: #ffffff`
- **Dark**: Add class `theme-dark` to `<body>`
- **High Contrast**: Add class `theme-hc` to `<body>`
- **Wireframe Mode**: Add class `wireframe-mode` to `<body>` for neutral greyscale

## Adding Screens

Each screen is a `<section class="screen" id="SCR-nnn">` with:

- **id**: Unique screen identifier (`SCR-001`, `SCR-002`, etc.)
- **data-label**: Human-readable screen name
- **data-device-frame**: Current device frame (web-desktop, ios-phone, etc.)
- **data-state**: Current screen state (default, loading, etc.)
- **data-persona**: Current user persona (user, admin, etc.)

Example:

```html
<section class="screen" id="SCR-001" data-label="Dashboard" data-device-frame="web-desktop">
  <div class="device-frame">
    <div class="device-frame-header">Dashboard</div>
    <div class="device-frame-content">
      <h1>Welcome</h1>
      <p>Your dashboard content here.</p>
    </div>
  </div>
</section>
```

## Screen States

Wrap content in state-specific divs:

```html
<div class="content-default" style="display: block;">
  <!-- Default state content -->
</div>
<div class="content-loading" style="display: none;">
  <!-- Loading spinner or placeholder -->
</div>
<div class="content-error" style="display: none;">
  <!-- Error message -->
</div>
```

The toggle automatically shows/hides content based on `data-state`.

## Internationalization (i18n)

The scaffold includes a minimal i18n system for UI labels. Customize the dictionary in `prototype.js`:

```javascript
this.i18n = {
  en: { /* English terms */ },
  nl: { /* Dutch terms */ },
  es: { /* Spanish terms */ },
};
```

Add more languages and terms as needed.

## Accessibility

- **Focus order**: Interactive elements are focusable; sidebar links and buttons have visible focus indicators.
- **Labels**: All form inputs have associated `<label>` elements.
- **Touch targets**: Buttons and links are at least 44x44px.
- **Reduced motion**: Respects `prefers-reduced-motion` media query.
- **Screen reader**: State changes announce via `aria-live="polite"`.
- **Color contrast**: Token pairs meet WCAG AA by default; high-contrast mode ensures 7:1 ratio.

## Device Frames

The prototype supports eight device frames:

| Frame | Width | Use |
|-------|-------|-----|
| `web-desktop` | 1024px | Desktop web browser |
| `web-tablet` | 768px | Tablet-sized web view |
| `web-mobile` | 375px | Mobile-sized responsive web |
| `ios-phone` | 390px | iOS phone (iPhone 14) |
| `android-phone` | 412px | Android phone (Pixel 7) |
| `tablet` | 768px | Generic tablet |
| `windows-window` | 900px | Windows desktop app |
| `macos-window` | 900px | macOS desktop app |

## Limitations

- No real data or API calls — use hardcoded sample content.
- No network requests — all assets must be local.
- No external dependencies or CDN — vanilla JavaScript only.
- Runs from `file://` URL scheme with no server required.

## Customization

### Change the accent color

Edit `tokens.css`:

```css
:root {
  --b-accent: #your-hex-color;
  --b-accent-dim: #lighter-variant;
}
```

### Add a new screen

1. Add a new `<section class="screen" id="SCR-nnn">` to `index.html`.
2. Add a link to the sidebar:
   ```html
   <li><a href="#SCR-nnn" class="screen-link" data-screen="SCR-nnn">SCR-nnn Name</a></li>
   ```

### Modify styles

All CSS is in `prototype.css`. Common changes:
- Font size: Edit `font-size: 14px` in `body`
- Spacing: Edit `padding` and `margin` values
- Sidebar width: Edit `--b-sidebar-w` in `tokens.css`

## License

Free to use and modify. Part of the product-discovery skill.
