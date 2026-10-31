# NEO-Zen Design System · v1

Shared visual contract for Today+, Five and Deadline Watch.

## Core principles

- **Shared shell:** center the desktop container at maximum **1220px** (not a 100%-width Five shell). Keep aligned brand mark, title, byline and top actions. Preserve each plugin's own interior needs.
- **Host font only:** every screen and control uses `var(--font-primary-stack)`, with system fallbacks covering Vietnamese. Do not bundle or download novelty fonts.
- **Host wallpaper:** `html`, `body`, root app containers and iframe canvases must remain transparent in the actual Super Productivity host. Use the host variables for theme text and surfaces, and translucent theme-aware *individual* panels rather than an opaque overlay.
- **NEO elements:** crisp 2px contrast-aware outlines, near-square corners, bold hierarchy, hard zero-blur 2–5px offset shadows, limited green / yellow / blue / coral / lilac accents. Use contrast-aware borders in dark mode, not permanently black outlines.
- **Zen behavior:** simple labels, spacious but not wasteful spacing, no aggressive animation, reduced-motion support and no interaction change during a visual redesign.
- **Accessibility:** focus-visible outlines, touch targets, functional states, and meaningful semantic labels. Keep original completion and drag-drop control identities.

## Plugin-specific exceptions

- **Today+:** tasks/subtasks and habits can show soft semi-transparent NEO tiles. Keep Not Today actions, habits, stopwatch time logging and grouping untouched.
- **Five:** preserve its five-item one-screen focus grid, completion-circle sizing and drag/drop/planning panels. Align outer shell and header with the family, but do not force the full-screen list to scroll or squash task metadata.
- **Deadline Watch:** can use stronger opaque, colorful individual cards since its dashboard is scroll-based, but the page canvas stays transparent.

## Release acceptance

Capture real browser screenshots using synthetic Vietnamese data at desktop, 390px and 320px; exercise light/dark wallpapers. CI must verify no horizontal overflow, no clipped title or progress controls, host font and transparent background, plus every plugin's feature regression tests. Only merge when checks pass, then automatically update the matching release ZIP without changing the plugin ID or version for design refinements.
