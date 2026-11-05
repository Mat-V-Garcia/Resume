# Resume Project

Web-based interactive resume for Mathew Garcia with modern glassmorphism design.

## Project Structure

- `index.html` - Single-file HTML resume with embedded CSS and JavaScript
- `Mathew_Garcia_Resume_Updated.docx` - Reference Word document for content

## Deployment

Hosted on GitHub Pages at: https://mat-v-garcia.github.io/Resume/

## Tech Stack

- Vanilla HTML/CSS/JavaScript (no frameworks)
- Google Fonts: Inter only (variable weight 400–700), with preconnect hints
- CSS custom properties for theming
- Canvas API for starfield animation

## Key Features

- **Themes**: Dark/light mode toggle with localStorage persistence
- **Glassmorphism**: Backdrop blur, semi-transparent cards, gradient overlays
  - Blur is switched off at ≤768px and under `prefers-reduced-transparency`; cards fall back to near-opaque backgrounds
- **Animations**:
  - Starfield particle background with mouse tracking (solid-disc stars, cached theme colors, pauses while the tab is hidden)
  - Flip cards for skills (CSS 3D transforms). Hover flips only on devices that can hover (`@media (hover: hover)`); click, tap, Enter and Space toggle the `.is-flipped` class and `aria-expanded`
  - Rotating 3D cubes for certifications (`aria-hidden`; the visible `.cert-title` below each cube carries the full name for screen readers and print)
  - Glow pulses on the header bar and timeline dots animate `opacity`, not `box-shadow`
- **Reduced motion**: starfield is static and skill cards show both faces stacked in flow
- **PDF Export**: Print-friendly styles via `@media print`
- **Responsive**: Mobile-first with clamp() and media queries

## Design System

### Colors (Dark Theme)
- Background: `#0f1419` to `#242d42`
- Accent: `#5B9FED` (blue)
- Text: White with varying opacity

### Colors (Light Theme)
- Background: `#f8fafb` to `#e8eef5`
- Accent: `#2563eb` (blue)
- Text: Dark with varying opacity
- Certification cube faces use a deep blue gradient (`#2563eb` to `#1d4ed8`) with white text for contrast

## Code Conventions

- CSS variables defined in `:root` and `[data-theme="light"]`
- BEM-like class naming (e.g., `.skill-card-front`, `.cert-cube-container`)
- No-blur fallback block at ~line 1409, print styles from ~line 1445 to the end of `<style>`
- JavaScript at end of `<body>` (~line 2209)

## Common Tasks

### Update Resume Content
Edit the HTML directly in `index.html`. Key sections (line numbers are approximate):
- Header: ~line 1902
- Summary: ~line 1913
- Skills: ~line 1921
- Experience: ~line 2023
- Certifications: ~line 2126
- Military: ~line 2194

### Modify Print Styles
Edit `@media print` block starting at ~line 1445. Key considerations:
- Hide animations, starfield, buttons
- Flatten 3D elements (cubes, flip cards)
- Use solid backgrounds for readability
- Keep `.cert-title` visible so the PDF names each certification

### Add New Skill Card
Copy an existing `.skill-card` div, including its `tabindex="0" role="button" aria-expanded="false"` attributes, and update:
- Icon SVG in `.skill-card-front`
- Title in `.skill-category-title`
- Skills in `.skill-list`
- Leave the `.skill-hint` span empty; its text ("Hover to reveal" / "Tap to reveal") comes from CSS

### Add New Certification
Copy an existing `.cert-cube-container` div, update the text in the `.cert-face` elements, and set the full name in the `<p class="cert-title">` after the cube.
