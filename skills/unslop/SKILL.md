---
name: unslop
description: "Audit and polish an existing landing page, dashboard, web app, or mobile screen when asked to clean up its visual design, remove an AI-generated look, or unslop the UI. Preserve product behavior and brand while improving hierarchy, spacing, copy, type, and interaction states. Not for prose-only cleanup or a new site build."
license: CC-BY-4.0
---

# Unslop

Improve the screen's craft and product identity without changing its purpose. Preserve features, navigation, section order, data semantics, accessibility, and working interactions unless the request explicitly includes redesigning them. Existing brand choices and design-system components are evidence, not flaws to erase.

## Inspect and choose the scope

Read the relevant source and design tokens. Identify the user, primary task, entry points, existing components, and constraints. Inspect the visible screen through the host's permitted verification tools when available. State when only code or a screenshot can be assessed.

For a screenshot-only input, audit what is visible. Build a reconstruction only if implementation was requested, and distinguish inferred behavior from observed behavior. For a live URL without editable source, give an audit; create a local prototype only when requested, and label it as a prototype rather than a deployed fix. Do not scrape or clone a site by default.

Use [the audit guide](references/audit.md) to record concrete issues with locations and their effect on the user's task. A gradient, emoji, serif, bold heading, or centered layout is not a defect by itself. Judge whether it competes with content, obscures meaning, breaks consistency, or mismatches the product.

- A strong screen may need no changes. Say so; do not invent a redesign.
- A few local issues call for focused polish within the existing design.
- Widespread issues may justify a coordinated pass across the named screen, within the request's scope.

State a short direction: product and audience, visual character, existing brand constraints, the one or two content areas that deserve emphasis, and a useful signature detail if one exists. A signature is optional, not new decoration. Ask only when a material brand or product choice cannot be inferred. Otherwise proceed with the authorized changes and make the assumptions visible.

## Improve in coherent passes

Read [the craft guide](references/craft.md) when choosing concrete treatments. Reuse existing tokens before adding values. Apply the relevant passes in this order, skipping categories without a demonstrated issue:

1. **Spacing:** align related edges, normalize sibling padding and row density, and make spacing reflect grouping.
2. **Color:** clarify surface and text roles. Reserve emphasis for actions, selection, meaningful data and status. Preserve semantic mappings and check contrast in the actual theme.
3. **Icons:** reuse one existing family with consistent size and alignment. Remove redundant decoration while keeping meaningful status and accessible names.
4. **Copy:** make labels and claims concrete. Preserve facts, legal copy, localization and accessible names. Flag unverified claims; never invent social proof or replace real data to make a screen prettier.
5. **Type:** clarify hierarchy with a small, readable scale and consistent numeric formats. Keep brand fonts, legibility and user font scaling.
6. **Layout:** improve proportions and reading order without losing information or actions. Keep real app density; support narrow screens, long labels and content growth.
7. **Details:** align radii and borders, simplify competing card treatments, and show useful chart comparisons. Retain hover, focus, active, loading, empty, error and disabled states where applicable.
8. **Visuals:** prefer the real product or meaningful content over decorative filler. Do not add an image unless it explains something. Read [media guidance](references/media.md) when imagery or a demonstration video is actually needed.
9. **Motion:** use it to explain feedback or state transitions. Remove distracting loops; honor reduced motion. Do not add animation just to make the redesign look active.

## Verify and report

Run checks appropriate to the changed files. When permitted, inspect the finished screen at representative desktop and narrow widths and exercise the affected primary path and keyboard navigation. On native mobile, use the host's device tools and platform conventions. Check overflow, focus visibility, text contrast, state handling and layout shifts. Never claim visual verification from a build or source inspection alone.

Follow the host's exact rules for browser, device and visual tools. In T3, use preview tools only when the request authorizes browser work, under the host's current rules. Otherwise use an existing permitted test harness; if it cannot provide visual evidence, report that limitation. Do not install a new browser stack or start a recording to work around host restrictions.

Compare against the original audit, not an arbitrary render count. Stop when the scoped issues are resolved and verified; expand only for a real regression or an unresolved requirement. Report the important changes, evidence, preserved constraints and remaining limits. Do not create a video, spend on a separate media service, publish, or deploy merely because the UI was polished.

Licensing details are retained in [the license notice](NOTICE.md).
