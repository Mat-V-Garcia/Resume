# Resume Project

Web-based interactive resume for Mathew Garcia with modern glassmorphism design.

## Project Structure

- `index.html` - Single-file HTML resume with embedded CSS and JavaScript
- `Mathew_Garcia_Resume_Updated.docx` - Reference Word document for content

## Deployment

Hosted on GitHub Pages at: https://mat-v-garcia.github.io/Resume/

## Tech Stack

- Vanilla HTML/CSS/JavaScript (no frameworks)
- Google Fonts: Inter, JetBrains Mono
- CSS custom properties for theming
- Canvas API for starfield animation

## Key Features

- **Themes**: Dark/light mode toggle with localStorage persistence
- **Glassmorphism**: Backdrop blur, semi-transparent cards, gradient overlays
- **Animations**:
  - Starfield particle background with mouse tracking
  - Flip cards for skills (CSS 3D transforms)
  - Rotating 3D cubes for certifications
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

## Code Conventions

- CSS variables defined in `:root` and `[data-theme="light"]`
- BEM-like class naming (e.g., `.skill-card-front`, `.cert-cube-container`)
- Print styles at end of `<style>` block (~line 1380)
- JavaScript at end of `<body>`

## Common Tasks

### Update Resume Content
Edit the HTML directly in `index.html`. Key sections:
- Header: ~line 1820
- Summary: ~line 1831
- Skills: ~line 1838
- Experience: ~line 1930
- Certifications: ~line 2040
- Military: ~line 2110

### Modify Print Styles
Edit `@media print` block starting at line 1380. Key considerations:
- Hide animations, starfield, buttons
- Flatten 3D elements (cubes, flip cards)
- Use solid backgrounds for readability

### Add New Skill Card
Copy existing `.skill-card` div and update:
- Icon SVG in `.skill-card-front`
- Title in `.skill-category-title`
- Skills in `.skill-list`

### Add New Certification
Copy existing `.cert-cube-container` div and update text in `.cert-face` elements.
