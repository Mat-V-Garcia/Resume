# Resume Project

Web-based interactive resume for Mathew Garcia with modern glassmorphism design.

## Project Structure

- `index.html` - Single-file HTML resume with embedded CSS and JavaScript
- `fonts/inter-latin-var.woff2` - Self-hosted Inter variable font (Latin subset, weights 100–900), the only font the page loads
- `fonts/LICENSE-Inter.txt` - SIL Open Font License for Inter (keep it next to the font)
- `Mathew_Garcia_Resume.docx` - Word version of the resume, generated from `index.html` by `tools/build_docx.py` (three Letter pages, Arial); regenerate it after any content change
- `Mathew_Garcia_Resume.pdf` - PDF of that Word file, exported by `tools/export_pdf.ps1`; regenerate it whenever the Word file changes
- `tools/build_docx.py` - Builds the Word file from the site. It uses the existing .docx as its own template, so styles, bullet numbering and fonts carry over unchanged
- `tools/export_pdf.ps1` - Exports the Word file to the PDF through Microsoft Word (Windows only)

The site's Download menu links to the PDF and the Word file by these names, so keep the names when regenerating them.

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
- **Contact chips** are the links themselves (email, LinkedIn, GitHub, all with `rel="noopener noreferrer"` where they open a new tab) with inline SVG icons instead of emoji; the phone number is deliberately not on the public page
- **Footer** links to GitHub and the live App Store and Google Play listings for MagisAI and Pray Serve
- **Head metadata**: description, theme-color, canonical, SVG favicon (data URI), Open Graph and Twitter tags, and a schema.org Person JSON-LD block
- **Downloads**: a fixed Download menu (`<details class="download-menu">`, its `<summary>` is the pill button) offers the repo's PDF and Word files, with `download` attributes naming them `Mathew_Garcia_Resume.pdf` and `.docx`, plus a "Print this page" option. Escape, a click outside and choosing an option close it; on phones it sits at the bottom-right as an icon and opens upward; it is hidden in print
- **PDF Export**: Print-friendly styles via `@media print`; `beforeprint` renames the document so a page saved from the print dialog is also called `Mathew_Garcia_Resume.pdf`
- **Responsive**: Mobile-first with clamp() and media queries

## Content Conventions

- Headline everywhere is "AI Product & Infrastructure Lead • Mobile + Cloud • FinOps": the `<title>`, the tagline, the meta description, the Open Graph tags and the summary all follow it. Change them together.
- Experience holds eight entries. The three concurrent roles are ordered Magis Center (primary employer), Stack 26 (products for the Diocese of Orange), MVG Consulting (FinOps and consulting); the rest are reverse chronological.
- Numbers in bullets come from Mat's own reports and repos (the September 2026 cost model, the October 2026 board deck, release notes, README evaluations). Do not add a figure without a source.
- Work shared with the MagisAI lab (the answer engine and corpus) is described as "co-built"; the app, gateway, Firebase, store pipeline, cost model and compliance work are Mat's.
- DPO is intentionally absent: the fine-tuning work used SFT, LoRA, QLoRA and RAFT.

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
- Inline head script at ~line 16, `@font-face` at ~line 31, download menu styles at ~line 204, no-blur fallback block at ~line 1494, print styles from ~line 1527 to the end of `<style>`
- Main JavaScript at end of `<body>` (~line 2356)

## Common Tasks

### Update Resume Content
Edit the HTML directly in `index.html`. Key sections (line numbers are approximate):
- Header: ~line 2003
- Summary: ~line 2022
- Skills: ~line 2030
- Experience: ~line 2132
- Certifications: ~line 2267
- Military: ~line 2335

When the headline or summary changes, update the `<meta name="description">`, the Open Graph description and the JSON-LD `jobTitle` in `<head>` to match. Wrap a standout number in `<span class="metric">` (keep the span short; it does not wrap). Then run `python tools/build_docx.py` so the Word file matches, and `powershell -ExecutionPolicy Bypass -File tools/export_pdf.ps1` so the PDF people download matches too.

### Regenerate the Word File and the PDF
Run `python tools/build_docx.py` from the repo root (Python 3, standard library only). It parses the header, summary, skill cards, experience entries, certification titles, military line and footer store links out of `index.html` and rewrites `Mathew_Garcia_Resume.docx` in place, keeping the old file's styles and numbering. The site is the source of truth; the Word-only choices live in the script:
- The header shows the city, not the street address or phone, because the file is public in this repo
- Section order is Summary, Certifications, Key Skills, Experience, Shipped Apps, Military
- Skill cards become "Category: items" bullets; the footer store links become the Shipped Apps list with hyperlinks
- The layout tunables at the top of the script (margins, heading spacing, type size, `keep_lines`) are set so the November 2026 content fills exactly three pages; `keep_lines=1` keeps bullets whole across page breaks but pushes the Military section onto a fourth page with the current content

`python tools/build_docx.py out=<path>` writes elsewhere without touching the repo copy, which is the way to try a layout change. Check the page count by opening the result in Word; there is no LibreOffice on this machine.

Then run `powershell -ExecutionPolicy Bypass -File tools/export_pdf.ps1` to export `Mathew_Garcia_Resume.pdf` from the Word file. It drives a hidden copy of Word with alerts switched off and quits it when done, in about fifteen seconds; the hyperlinks survive the export. Keep the `[string]` casts on the paths in that script: a path handed to Word straight from `Join-Path` makes the export call wait forever, and the only way out is to stop the hidden `WINWORD.EXE`.

### Modify Print Styles
Edit `@media print` block starting at ~line 1527. The settings are already tight: a 10pt base, compact card and bullet spacing, a three-column skills grid, cards that may break across pages while each job header stays with its bullets, and the Military section held with the certifications. With the November 2026 content the printed page runs four Letter pages; it was three before the content grew. Fewer bullets, not more CSS, is what would bring it back to three. Since the Download menu serves the three-page Word export as the PDF, the printed length only matters to people who choose "Print this page". Key considerations:
- Hide animations, starfield, buttons
- Flatten 3D elements (cubes, flip cards)
- Use solid backgrounds for readability
- Keep `.cert-title` visible so the PDF names each certification

### Add New Skill Card
Copy an existing `.skill-card` div, including its `tabindex="0" role="button" aria-expanded="false"` attributes, and update:
- Icon SVG in `.skill-card-front` (keep `aria-hidden="true" focusable="false"`)
- Title in `.skill-category-title`
- Skills in `.skill-list` (about 120 characters fits the card at every width)
- Leave the `.skill-hint` span empty; its text ("Hover to reveal" / "Tap to reveal") comes from CSS

The grid is balanced at six cards; a seventh leaves an orphan row.

### Add New Certification
Copy an existing `.cert-cube-container` div, update the text in the `.cert-face` elements, and set the full name in the `<p class="cert-title">` after the cube.

### Replace the Font
Drop a new woff2 into `fonts/`, update the `@font-face` `src` and the `<link rel="preload">` in `<head>`, and keep the font's license file beside it.
