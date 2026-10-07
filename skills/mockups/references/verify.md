# Verify

Judge from evidence: rendered pixels, observed interaction, audit output. Not from rereading your own code.

## 1. Run the audit

```bash
node <skill-dir>/scripts/run.mjs .mockups/<slug>/index.html
```

It renders in headless Chrome at 375, 768 and 1280 for every state, runs `scripts/audit.js`, saves screenshots, and prints one report: ERROR and warn lines with where each occurs, plus screenshot paths. It needs Node 22+ and Chrome (`CHROME_PATH` overrides the location). With the T3 preview tools, you can instead open the file and pass the contents of `scripts/audit.js` to `preview_evaluate`.

Exit codes: `0` means no audit errors, script exceptions or incomplete screenshots; `1` means findings require attention; `2` means rendering or invocation failed. Warnings still require judgment. `--report-only` suppresses findings exit failures, not rendering failures. Font/image readiness and browser requests have bounded waits; use `--timeout-ms` for a legitimately slow local asset load.

Screenshots capture up to 12,000px by default. An `INCOMPLETE screenshot` line identifies a clipped page; increase `--max-height` or inspect the remaining page separately. `TRUNCATED findings` reports omitted repeated findings; do not treat the displayed list as exhaustive.

The audit is heuristic, not a WCAG certification. Contrast on images/gradients and keyboard-focus visibility require manual inspection. Small-target warnings express design preferences; evaluate spacing and WCAG exceptions before calling them compliance failures.

## 2. Look

Read the screenshots: the ideal state at every width, and every other state at 1280. Fixed and sticky bars appear at their viewport position in full-page captures, so judge them in the first screen. For each width, answer:

- What does the eye hit first, and is it the primary thing?
- Five-second test: what is this, what can I do, what happens next?
- Is the rhythm consistent (spacing, alignment, density)? Is any text clipped or crowded?
- Is each state well made, not just present?
- Does every native control (checkbox, select, date input, scrollbar) look designed for this theme, not browser default?
- For an existing product: set it beside the Ground screenshot. Does it look like the same product?

## 3. Interact

In a live page (T3 preview tools, or the user's browser), complete the main flow, trigger one error path, tab through with the keyboard only, press Escape on any overlay. Each finding cites a screenshot, an audit line, or an observed result.

## 4. Fix once

Fix every ERROR and every observed defect in a single pass, run the audit again, then stop. Anything left goes into the hand off as a known issue. Do not loop for polish.

## Hand off

- Path of the file and how to switch states.
- Decisions and the evidence for each (project fact, user need, or precedent with link).
- Assumptions still unconfirmed.
- What is mocked or does nothing.
- Open questions and known issues.

Stop any server you started.
