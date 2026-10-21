# Visuals: aid a visual learner without ASCII art

## Decision table
| Content shape | Visual | Tool |
|---|---|---|
| Sequential process (3–7 steps) | Horizontal flow of coloured boxes with ➜ | HTML/CSS `.flow` |
| Process with a decision or loop | Flowchart (diamond, back-edge) | Graphviz `dot` |
| Layered architecture (stack) | Stacked colour bands, labelled bottom-up | HTML/CSS `.stack` |
| 2×2 matrix (e.g. Pisano, BCG) | Coloured grid with axis labels | HTML/CSS `.pisano` grid |
| Comparison of 2–4 options | Table with a navy header | HTML table |
| Timeline / eras | 3–5 era cards, or a matplotlib timeline | CSS `.timeline` |
| Trend over time / amounts | Bar or line chart with annotated peaks | matplotlib |
| Money split / fee breakdown | Waterfall chart | matplotlib |
| Shares of a whole | Single stacked horizontal bar (avoid pies) | matplotlib |
| Platform / network relationships | Node-edge diagram with labelled edges | Graphviz |
| Cycle / flywheel | Circular layout | Graphviz `circo` (keep it small) |
| Data-structure picture (blocks, records) | HTML-like record tables in Graphviz | Graphviz |
| Concept illustration (scene, metaphor) | Generated image, non-artistic | Image backend (see `image-generation.md`) |

## Rules
- **No ASCII art, ever.**
- Keep diagrams **narrow enough** that, scaled to the ~180 mm text width, labels stay ≥ 8 pt. Long left-to-right chains of more than 5 nodes become tiny; wrap them, switch to top-to-bottom, or use a CSS flow (which wraps automatically).
- Graphviz with HTML labels eats spaces next to `<b>` tags: replace `" <b>"` with `"&#160;<b>"` and `"</b> "` with `"</b>&#160;"` before rendering (see the example script).
- In matplotlib, `$` starts mathtext: escape it as `\$` in titles and labels.
- Use the palette consistently: blue `#2E6FD8` (default / concepts), teal `#0F9D8A` (positive / new / FinTech side), orange `#E07B26` (highlight / money), red `#C8483B` (risk / incumbent pain / traps), purple `#7A5AC8` (memory / AI), navy `#1F3A5F` (headers / final step), grey `#6B7A90` (neutral). Light fills with a darker border: `#E6EEFB`, `#E2F4F1`, `#FDEEDF`, `#FBE6E3`, `#EEE8FA`.
- Font: Inter (or the system sans-serif). Same family in diagrams and body.
- Every figure gets a short caption saying what to notice ("Edit one block → its hash changes → the link breaks").
- Render SVG for charts and diagrams (crisp in the PDF). Preview with `scripts/page_sheets.py` after building.

## Sizing classes (in `study-guide.css`)
`figure.w100 / w90 / w80 / w70 / w60 / w50`: pick so the diagram's smallest text stays readable and the figure doesn't create a mostly-empty page.
