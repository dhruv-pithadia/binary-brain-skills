# Build

One self-contained HTML file at `.mockups/<feature-slug>/index.html`: inline CSS and JS, no build step, no frameworks. Copy any assets (fonts, images) beside it and reference them relatively. Write it once, then edit in place for feedback.

## Identity

**Existing product.** Reproduce the project's real tokens: copy values, not approximations. Name the CSS variables as the project does. Use the project's fonts from the same source it uses; if that is unavailable offline, fall back and say so. Reuse its component markup and class idioms. Departing from the product's own patterns needs a UX reason (a new interaction needs a new component); otherwise match.

**Greenfield.** Use the identity direction selected from the brief or Diverge. Write one line of rationale per decision (type, color, shape, density, motion, imagery), each citing an audience, domain or brand fact; if you cannot cite one, widen research or ask. Check: swap in a different product's name and domain; if the design still fits, it is generic.

**Before writing CSS.** State the project or user fact that justifies any departure from established patterns. Matching an existing product is correct.

## Experience

- **Real content.** Realistic names, numbers and lengths taken from the project's types. Include one long value, one short, one large number; add non-Latin or right-to-left text if the product is international. Write copy in the product's voice, with button labels that name the outcome. No lorem ipsum, no "Item 1".
- **States.** Mark each with `data-state-view` and inline `scripts/states.js` at the end of `<body>`. Cover: ideal; empty (first use, cleared, and no results are different); loading (skeleton matching the final layout); partial (some data missing); error (what happened, what to do, user's input preserved). Add the feature's own: success, permission denied, offline, destructive confirmation. Include the states relevant to the requested flow; reuse existing states for small changes and state meaningful omissions in the handoff.
- **Interaction.** The main flow is clickable with small inline JS. Controls show hover, focus, active, and disabled with a visible reason. Keyboard order is logical, Escape closes overlays, focus returns to the trigger. Forms validate inline with the message attached to the field. A control that does nothing is listed in the hand off.
- **Accessibility baseline.** Semantic elements (button, a, nav, main, label, table), accessible names, a visible `:focus-visible` style, contrast 4.5:1 for text and 3:1 for large text and UI parts, targets at least 24px (44px on phones), meaning never carried by color alone, `prefers-reduced-motion` respected, `lang`, viewport meta, one h1 with ordered headings.
- **Responsive.** Works at 375, 768 and 1280 without horizontal scroll. Decide what changes per width; do not just shrink.
- **Native controls.** Style checkboxes, radios, selects, inputs and scrollbars to the theme (`accent-color`, `appearance`, custom markup). Set `color-scheme: dark` on a dark theme so defaults are not white.
- **Motion.** Only to explain a change (appear, move, confirm). Around 150 to 250ms.

## Mobile features

Constrain content to a phone-width column centered on the project's background. Follow the platform's conventions (iOS or Material) where the product does.
