# Craft guide

Use the project's system first. These are starting points for missing decisions, not mandatory replacements or accessibility guarantees.

## Rhythm and density

A 4px spacing rhythm, with 2px optical adjustments inside compact controls, often reduces one-off values. Useful spacing steps include 4, 8, 12, 16, 24, 32, 48 and 64px. Keep gaps within a group smaller than those between groups. Let content, platform touch-target guidance and text scaling determine control heights; do not shrink targets just to fit a reference.

## Surfaces and attention

Define roles for page, card, raised surface, border, primary text, secondary text and muted metadata. Use a coherent palette for those roles. In a dense app, quiet surfaces make content easier to scan; an expressive landing page can use more color when the brand calls for it. Accent and semantic colors serve different purposes. Validate contrast on the actual background, including focus rings and disabled-state distinctions.

Reduce competing effects before adding new ones. Depth can come from surface separation, borders or restrained shadows. Gradients and bright colors remain appropriate when they communicate identity or meaning and maintain legibility.

## Type and icons

Prefer existing font assets. Use a few recurring text sizes and weights instead of arbitrary values. Make headings readable at narrow widths without making every heading thin. Keep small text comfortably readable and avoid aggressive negative tracking. Use tabular figures where columns or live numbers need alignment, while preserving locale and precision.

Reuse the project's icon set and semantic labels. Align icon boxes and baselines. Decorative icons should not introduce extra screen-reader output; icon-only controls need accessible names. Do not add a package solely to replace a few already-consistent icons.

## Structure and data

Reuse established cards, inputs and navigation before inventing wrappers. Size corners to the component and its padding; inner and outer curves should look related. Let chart choice follow the question: trends, comparisons, proportions or progress. Give the most important information a clear hierarchy without suppressing useful comparisons. Preserve a table or accessible alternative when needed.

## Motion

Prefer existing motion tokens. Short feedback transitions often work around 120–220ms; larger state changes may need longer. Favor transform and opacity when appropriate, but preserve correct layout and usability over a blanket animation rule. Avoid `transition-all`. Disable nonessential animation for reduced-motion users and pause expensive off-screen effects.
