---
name: study-synthesizer
description: Turn a folder of course materials (slides, PDFs, course policy, textbook, past papers, rough notes) into a final, exam-ready visual study guide PDF with unit-by-unit frameworks, diagrams, cases, key numbers, mnemonics, exam traps, model answers and a cheat sheet, plus an optional past-paper question bank. Use when the user asks to make a study guide, revision notes, exam prep report or question bank from their course files.
---

# Study Synthesizer

Turns a folder of study material into **one polished, visual, exam-ready PDF** that a visual learner can revise from the night before an exam. The output should feel like a great senior's notes: one story across the course, every idea with a picture, every number checked against the sources, and every unit ending in exam practice.

This skill is **agent-agnostic**. Any coding agent that can read files and run a shell (Claude Code, Codex, Cursor, Gemini CLI, Windsurf, etc.) can follow it. Only **image generation** has a preferred backend (GPT via the Codex CLI), and it always has a fallback, so the skill never dead-ends. See `references/agent-adapters.md` for host-specific notes.

## Non-negotiables

1. **The sources are the truth.** Every fact, number, date and example in the guide must come from the user's materials or from verified research. Never invent statistics. When the draft and the slides disagree, the slides and textbook win; tell the user what you corrected.
2. **Visual first, never ASCII.** No ASCII boxes or arrows anywhere. Every framework, flow, stack, comparison or trend becomes a real diagram, chart, styled table or CSS flow (see `references/visuals.md`).
3. **Non-artistic images.** Any generated image must be flat, clean, labelled and diagram-like. No painterly, cinematic or "concept art" styles; legibility beats beauty.
4. **Honest about gaps.** If something can't be read (a scanned page that fails OCR), can't be reached (no image backend, no web) or isn't in the sources, say so in the final summary. Never hide it.
5. **Check before delivering.** Look at every rendered page, re-run every calculation and check every number against its source before you hand over the PDF.

## Workflow

Track these phases in the host's task list if it has one. Ask the user at most one round of questions, and only if the scope is truly unclear (e.g. which exam: midterm units 1–7, or the final?). Otherwise make sensible defaults, state them at the top of your summary, and proceed.

### Phase 0 · Set up and detect capabilities
- Create a working directory outside the user's folder (never edit their originals). Write outputs back next to the inputs only at the end.
- Run `scripts/detect_env.sh`. It reports: PDF tools (pdftotext, pdftoppm), office conversion (LibreOffice), Python libraries (python-pptx, matplotlib), Graphviz, a headless Chromium / Playwright for PDF rendering, the Codex CLI and its login status, and `OPENAI_API_KEY`. Install what's missing if the host allows it. Record the image backend you will use (see Phase 7).

### Phase 1 · Inventory and ingest everything
- Run `python3 scripts/ingest.py <materials_folder> <workdir>`. It lists every file, extracts text from PDFs / PPTX / DOCX / MD / TXT, flags **scanned PDFs** and **image-only slides**, and renders those to PNG so you can read them visually.
- **Read the rendered images** for scanned pages and image-only slides. Lecture decks often carry key tables, charts and case facts only as pictures; skipping them loses content.
- Classify every file: `course-policy/syllabus`, `lecture-slides`, `textbook`, `past-papers`, `user-draft`, `notes`, `other`. Details: `references/ingestion.md`.

### Phase 2 · Build the course map
- From the course policy / syllabus, extract: course code, unit list with titles, course outcomes (COs), exam scheme (marks, duration, compulsory questions, choice), prescribed textbook and references.
- Decide the **scope** (e.g. midterm = Units 1–7) from the user's request; default to everything taught so far.
- Map each slide deck and textbook chapter to its unit. Record the mapping in `workdir/course_map.md`.

### Phase 3 · Research (any available model or tool)
Use whatever research ability the host has: web search, a research subagent, or the agent's own browsing. No specific model is required. Goals, in priority order:
1. **Check relevance:** confirm each source belongs to this course and syllabus version (flag outdated decks and old-syllabus papers).
2. **Verify volatile facts:** anything that changes over time (market sizes, regulations, latest stats, who runs what) must be checked against a current source and cited.
3. **Fill thin spots:** where the slides are skeletal, find the standard explanation (textbook first, then reputable sources such as regulators, central banks, official docs, university notes; YouTube lectures only for intuition, never as a sole source for facts).

Write `workdir/research_brief.md` with findings, sources (URLs) and a "verified / unverified" flag per fact. If no web access exists, note "research skipped: offline" and rely on the course materials only. Details: `references/research.md`.

### Phase 4 · Audit the user's draft (if one exists)
Treat the draft as raw input, not as truth:
- Keep its good structure, examples and model answers.
- Cross-check against the slides and textbook: fix wrong numbers, wrong definitions and invented examples, and replace any calculation that doesn't match the course's version (e.g. the lecturer's worked example).
- List what the draft **missed** that the slides cover. These become "Added from slides" boxes in the guide.
- Strip ASCII diagrams and replace each with a real visual in Phase 7.
If there's no draft, build from the materials directly.

### Phase 5 · Past papers (if any)
If past papers exist, read every question (render scans), tag each with its unit (or "later unit / out of syllabus"), count how often each topic appears, and note the exam pattern. Use this to:
- add an **exam-practice** block to each unit that answers the real questions asked, and
- optionally produce a separate **Question Bank PDF** (coverage table, frequency chart, model answers with frameworks, likely variants, last-minute kit).
Method and answer format: `references/past-papers.md`.

### Phase 6 · Write the guide
Follow `references/report-structure.md` (whole document) and `references/unit-template.md` (every unit). In short:
- **Front matter:** cover → how to use → "the story of the course" (one flow showing how units connect) → cross-cutting ideas → how to write a long answer.
- **Each unit:** opener with tier tag → one-line idea → concepts with diagrams → cases and key numbers → mnemonic → exam traps → "Added from slides" → exam practice (model answers) → 60-second recall checklist.
- **End matter:** night-before cheat sheet (all mnemonics, formulas, numbers to quote, case → concept map), acronym glossary, final readiness checklist.
Write in **plain, short sentences**, define every acronym on first use, and always pair a framework with an example and a number.

### Phase 7 · Visuals
1. **Plan** one visual for every framework, process, comparison, stack, timeline or dataset (`references/visuals.md` has the decision table).
2. **Precise diagrams in code (always):** Graphviz for flows and structures, matplotlib for charts, HTML/CSS for flows, stacks, 2×2 grids, timelines and tables. These are exact, editable and never misspell labels. Starters: `scripts/diagrams_example.py`, `scripts/charts_example.py`.
3. **Illustrative images (optional, where a picture genuinely helps understanding):** use the image backend chain in `references/image-generation.md`:
   - **Preferred:** GPT image generation via the **Codex CLI** (`scripts/gen_image_codex.sh`, model from `STUDY_SYNTH_IMAGE_MODEL`, default `gpt-6.1-sol`).
   - **Fallback 1:** the host agent's own built-in image-generation tool, if it has one.
   - **Fallback 2:** the OpenAI Images API, if `OPENAI_API_KEY` is set (`scripts/gen_image_api.py`).
   - **Fallback 3:** no image model available → draw it as a code diagram instead and mention this in the summary.
   Always use the non-artistic prompt template. **Inspect every generated image** before using it; reject any with garbled text, wrong labels or decorative clutter.

### Phase 8 · Build the PDF
- Assemble HTML parts (one file per section) using `assets/study-guide.css` and the components in `assets/components.html`.
- Render with `python3 scripts/build_pdf.py <parts_dir> <out.pdf>` (Playwright Chromium; falls back to headless Chrome `--print-to-pdf`).
- A4, page numbers, each unit starting on a new page, boxes and figures that don't split across pages.

### Phase 9 · Structural and factual QA (mandatory)
Run `python3 scripts/page_sheets.py <out.pdf> <workdir/qa>` and **look at every contact sheet**, then zoom into suspicious pages. Fix and rebuild until clean. Full checklist: `references/qa-checklist.md`. Minimum:
- no text overflow, clipped tables, overlapping labels or unreadable small text;
- no near-empty pages (an orphaned line or box spilling onto its own page);
- no headings stranded at the bottom of a page;
- diagrams sized so their text is ≥ ~8pt on the page;
- every number matches its source; every calculation recomputed; every acronym defined.
If the host supports subagents, a **fresh subagent** may do this review so the work isn't grading itself; otherwise do it yourself, carefully.

### Phase 10 · Deliver
- Save the PDF (and the question bank, if made) next to the user's materials, or where they asked. Keep the HTML source and diagram scripts in a `_study_synth_src/` folder so the user can regenerate it.
- Summary for the user (short): what was produced, page count, scope covered, what was **added or corrected** versus their draft, which image backend was used (or why not), anything that couldn't be read or verified, and sources for any researched facts.

## Files in this skill
| Path | Purpose |
|---|---|
| `references/report-structure.md` | Whole-document blueprint (front matter, units, end matter) |
| `references/unit-template.md` | The per-unit pattern and writing rules |
| `references/visuals.md` | When to use which visual; palette; diagram rules |
| `references/image-generation.md` | Codex CLI → host tool → API → code fallback chain; prompt template |
| `references/past-papers.md` | Past-paper mapping, frequency analysis, question-bank format |
| `references/research.md` | Research scope, source quality, brief format |
| `references/ingestion.md` | Reading every file type, including scans and image-only slides |
| `references/qa-checklist.md` | Structural and factual QA checklist |
| `references/agent-adapters.md` | Notes for Claude Code, Codex, Cursor, Gemini CLI and others |
| `assets/study-guide.css` | Print stylesheet (A4, colour-coded boxes, tables, flows, stacks) |
| `assets/components.html` | Copy-paste HTML components (unit opener, boxes, flow, stack, 2×2, Q&A, recall) |
| `scripts/detect_env.sh` | Capability and image-backend detection |
| `scripts/ingest.py` | Inventory + text extraction + render scans and image-only slides |
| `scripts/gen_image_codex.sh` | Generate one image via the Codex CLI (preferred backend) |
| `scripts/gen_image_api.py` | Fallback image generation via the OpenAI Images API |
| `scripts/build_pdf.py` | HTML parts → PDF |
| `scripts/page_sheets.py` | PDF → page contact sheets for visual QA |
| `scripts/diagrams_example.py` | Graphviz starter (flows, platforms, hash chain, stacks) with the label-spacing fix |
| `scripts/charts_example.py` | matplotlib starter (trend bars, waterfall, 2-axis, comparison bars) |
| `assets/examples/` | Reference outputs: `reference-study-guide.pdf`, `reference-question-bank.pdf` |
| `agents/openai.yaml` | Optional Codex UI metadata |
