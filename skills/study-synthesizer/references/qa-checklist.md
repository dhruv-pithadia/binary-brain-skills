# QA checklist: run before delivering

Run `python3 scripts/page_sheets.py out.pdf qa/` → open every `sheet*.jpg`, then zoom into any doubtful page with `pdftoppm -r 80 -f N -l N`.

## Structure and layout
- [ ] No text overflowing boxes, table cells or the page edge.
- [ ] No near-empty pages (a lone line, box or caption spilled over). Fix by shrinking a figure (`w90 → w70`), moving a box, or allowing a long Q&A to split.
- [ ] No heading left at the bottom of a page with its content on the next (`break-after: avoid` on headings).
- [ ] Each unit starts on a new page; the cover is full-bleed; page numbers show on content pages.
- [ ] Diagrams readable: smallest label ≥ ~8 pt at print size; no diagram scaled into a thin strip.
- [ ] Flows wrap cleanly; no arrow orphaned at a line end.
- [ ] Tables: header row present, columns not crushed, no row split mid-way (`tr { break-inside: avoid }`).
- [ ] Colour contrast is fine (dark text on light fills; white text only on navy or strong colours).
- [ ] No ASCII art left anywhere (search the HTML for `+---`, `|  |`, `-->` inside `<pre>`).
- [ ] Generated images: correct labels, no garbled text, non-artistic.

## Content and facts
- [ ] Every number traced to a source (materials or `research_brief.md`); volatile ones are cited.
- [ ] Every calculation recomputed in code (`python3 -c`) and shown with its working.
- [ ] Every acronym expanded on first use and listed in the glossary.
- [ ] Mnemonics match their lists exactly (letters, order, no mixed categories).
- [ ] Each unit has: one-line idea, ≥ 1 diagram, key numbers, cases, mnemonic, exam practice, recall checklist.
- [ ] "Added from slides" boxes really are absent from the user's draft.
- [ ] Draft errors corrected and listed for the summary.
- [ ] Scope matches the request (e.g. Units 1–7 only; later units are clearly labelled if included).

## Independent review (when possible)
If the host supports subagents or another model, give a fresh reviewer the PDF + this checklist + the sources folder, and ask for a list of defects with page numbers. Fix them, rebuild, and re-check only the affected pages.
