# Resume Project

Web-based interactive resume for Mathew Garcia with modern glassmorphism design.

## Project Structure

- `index.html` - Single-file HTML resume with embedded CSS and JavaScript
- `fonts/inter-latin-var.woff2` - Self-hosted Inter variable font (Latin subset, weights 100–900), the only font the page loads
- `fonts/LICENSE-Inter.txt` - SIL Open Font License for Inter (keep it next to the font)
- `Mathew_Garcia_Resume_Updated.docx` - Reference Word document for content

## Deployment

Hosted on GitHub Pages at: https://mat-v-garcia.github.io/Resume/

## Tech Stack

- Vanilla HTML/CSS/JavaScript (no frameworks, no third-party requests at all)
- Inter via an inline `@font-face` plus a `<link rel="preload">`; nothing is fetched from Google Fonts
- CSS custom properties for theming
- Canvas API for starfield animation

## Key Features

- **Themes**: Dark/light mode toggle with localStorage persistence
  - An inline script in `<head>` applies the stored theme (or the OS preference) before first paint, so there is no flash
  - All `localStorage` access goes through the `store` helper, which swallows errors when site data is blocked
  - The toggle's `aria-label` announces what it will switch to
- **Glassmorphism**: Backdrop blur, semi-transparent cards, gradient overlays
  - Blur is switched off at ≤768px and under `prefers-reduced-transparency`; cards fall back to near-opaque backgrounds
- **Animations**:
  - Starfield particle background with mouse tracking (solid-disc stars, cached theme colors, pauses while the tab is hidden, stars reshuffle only when the width changes)
  - Flip cards for skills (CSS 3D transforms). Hover flips only on devices that can hover (`@media (hover: hover)`); click, tap, Enter and Space toggle the `.is-flipped` class and `aria-expanded`
  - Rotating 3D cubes for certifications (`aria-hidden`; the visible `.cert-title` below each cube carries the full name for screen readers and print)
  - Glow pulses on the header bar and timeline dots animate `opacity`, not `box-shadow`
- **Reduced motion**: starfield is static and skill cards show both faces stacked in flow
- **Semantics**: `<main>`, `<header>`, one `<section aria-labelledby>` per card, `<footer>`, `<h3>` job titles; decorative SVGs and the canvas are `aria-hidden`
- **Contact chips** are the links themselves (`tel:`, `mailto:`, LinkedIn with `rel="noopener noreferrer"`) with inline SVG icons instead of emoji
- **Head metadata**: description, theme-color, canonical, SVG favicon (data URI), Open Graph and Twitter tags, and a schema.org Person JSON-LD block
- **PDF Export**: Print-friendly styles via `@media print`; `beforeprint` renames the document so the saved file is `Mathew_Garcia_Resume.pdf`
- **Responsive**: Mobile-first with clamp() and media queries

## Design System

### Colors (Dark Theme)
- Background: `#0f1419` to `#242d42`
- Accent: `#5B9FED` (blue)
- Text: White with varying opacity (`--text-muted` is 60% so small text stays readable)

### Colors (Light Theme)
- Background: `#f8fafb` to `#e8eef5`
- Accent: `#2563eb` (blue)
- Text: Dark with varying opacity (`--text-tertiary` 66%, `--text-muted` 62%)
- Certification cube faces use a deep blue gradient (`#2563eb` to `#1d4ed8`) with white text for contrast
- Metric highlights are `#047857` in light mode

## Code Conventions

- CSS variables defined in `:root` and `[data-theme="light"]`; unused tokens have been removed, so add one only when it is used
- BEM-like class naming (e.g., `.skill-card-front`, `.cert-cube-container`)
- `transition` lists name their properties explicitly; do not use `transition: all`
- Page-break control uses the modern `break-*` properties
- Inline head script at ~line 16, `@font-face` at ~line 31, no-blur fallback block at ~line 1395, print styles from ~line 1431 to the end of `<style>`
- Main JavaScript at end of `<body>` (~line 2203)

## Common Tasks

### Update Resume Content
Edit the HTML directly in `index.html`. Key sections (line numbers are approximate):
- Header: ~line 1887
- Summary: ~line 1907
- Skills: ~line 1915
- Experience: ~line 2017
- Certifications: ~line 2120
- Military: ~line 2188

When the headline or summary changes, update the `<meta name="description">`, the Open Graph description and the JSON-LD `jobTitle` in `<head>` to match.

### Modify Print Styles
Edit `@media print` block starting at ~line 1431. The current settings produce three Letter pages: a 10pt base, tightened card and bullet spacing, a three-column skills grid, cards that may break across pages while each job header stays with its bullets, and the Military section held with the certifications. Key considerations:
- Hide animations, starfield, buttons
- Flatten 3D elements (cubes, flip cards)
- Use solid backgrounds for readability
- Keep `.cert-title` visible so the PDF names each certification
- Two pages would need fewer bullets, not more CSS

### Add New Skill Card
Copy an existing `.skill-card` div, including its `tabindex="0" role="button" aria-expanded="false"` attributes, and update:
- Icon SVG in `.skill-card-front` (keep `aria-hidden="true" focusable="false"`)
- Title in `.skill-category-title`
- Skills in `.skill-list`
- Leave the `.skill-hint` span empty; its text ("Hover to reveal" / "Tap to reveal") comes from CSS

### Add New Certification
Copy an existing `.cert-cube-container` div, update the text in the `.cert-face` elements, and set the full name in the `<p class="cert-title">` after the cube.

### Replace the Font
Drop a new woff2 into `fonts/`, update the `@font-face` `src` and the `<link rel="preload">` in `<head>`, and keep the font's license file beside it.
