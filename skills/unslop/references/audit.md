# Audit guide

Record each finding as location, observed issue, user impact, and smallest useful correction. Separate observed defects from taste and suggestions. Inspect only categories relevant to the screen.

- **Attention:** Do background effects, badges, saturated borders or repeated highlights compete with the task? Is the primary action easy to find? Does each semantic color retain a consistent meaning?
- **Typography:** Are hierarchy and scanning clear? Check small text, line length, long labels, inconsistent weights and number formats. Dense labels need legibility, not automatic uppercase removal.
- **Spacing:** Compare sibling rows and cards, icon columns, label baselines and group boundaries. Prefer shared tokens to isolated margin nudges. Optical corrections can be legitimate.
- **Copy:** Identify generic headlines, redundant labels, unsupported metrics and ambiguous comparisons. Preserve real claims pending verification rather than silently replacing facts. Mock data belongs only in clearly identified examples.
- **Components:** Look for redundant pills, status represented by color alone, inconsistent radii and decorative mini-charts. Keep repeated structures when they help comparison; asymmetry is not a goal by itself.
- **Layout:** Check usable content width, reading order, action placement and space consumed by navigation. A dashboard should remain a working dashboard rather than become a marketing hero.
- **Data:** Check units, legends, time windows, baselines and missing states. Do not alter values, reorder meaningful categories, smooth away variation, or remove a useful series for aesthetics.
- **Visuals:** Can the image explain its relationship to the product? Check text embedded in images, sharpness, cropping, responsive fit and alternative text. Decorative images need empty alternative text.
- **Interaction:** Exercise keyboard focus, touch targets, hover and press feedback, loading and error recovery. Remove meaningless pulsing while retaining necessary progress and live-status feedback.
- **Brand:** Confirm the proposed correction fits the existing logo, palette, type and audience. Do not apply a universal neutral theme or replace an intentional identity with another template.

When findings are minor, keep the existing composition. A large visual change needs a correspondingly clear benefit.
