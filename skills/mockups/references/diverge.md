# Diverge

Purpose: put structurally different answers in front of the user before any visual work. Changing a button color is not a different answer.

## Skip when

The interaction pattern is already established in the project (add a column to this table) or the user said to skip. State why in one line and go to Build.

## 1. Map the answer space

List about five candidate approaches. For each, estimate the probability that a typical designer, or you on autopilot, would pick it (sum near 1). Typicality is a map of where the crowd is, not a verdict. Typical answers are often right; you need to know where they sit.

## 2. Choose three along one named axis

Pick the axis the brief makes most consequential:

- Where it lives: page, panel, inline, modal, command.
- How much shows at once: everything, progressive, on demand.
- Who is in control: user-driven, suggested, automatic.
- When it appears: upfront, in the moment, after the fact.
- Representation: list, form, canvas, conversation.
- Commitment: preview then apply, or apply directly with undo.

Rules: the three must differ in a way a user would notice within five seconds, otherwise merge them. At least one has typicality under 0.2 and still satisfies the brief's constraints; label it as the unconventional option.

## 3. Breadboard each in words (at most eight lines)

- **Places:** screens or panels involved.
- **Affordances:** what the user can do in each.
- **Flow:** `A -> B on <action>`.
- Then: best for, costs, which brief scenarios it handles well or badly (happy, empty, worst case), and fit with the project's existing patterns.

Judge with: visible system status, user control and undo, error prevention, recognition over recall, consistency with the product.

## 4. Recommend

List the options without ranking, then give your recommendation and reasons tied to the brief. Ask the user to pick, merge, or request a different axis.

## 5. Greenfield only: identity options

Runs even when steps 1 to 4 were skipped. When Ground found no design system, identity is also a decision with alternatives. List four identity directions in one line each (palette temperature, type voice, density, shape language) with a typicality estimate. Choose the one the audience and setting justify. Include one under 0.2 and either choose it or name the fact that rules it out. Warm paper tones, system sans and one teal or green accent are the common answer; pick them only if the facts point there. This list goes into the hand off.

## Low-fi visuals (only when space is what differs)

If the options differ in spatial layout (dashboards, canvases, multi-pane tools), also write `options.html`: one file, one tab per option, grayscale only, system font, labeled boxes with real copy, no brand styling, same state switcher. When the options differ in flow or logic, words are enough.
