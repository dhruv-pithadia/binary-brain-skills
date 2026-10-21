# Ingestion: read everything, including what's only in pictures

## File types
| Type | How to read | Watch out for |
|---|---|---|
| PDF (text) | `pdftotext -layout` | Columns and tables may scramble; check against a page image for key tables |
| PDF (scanned) | `pdftoppm -r 110 -png` → read the images (or OCR with `tesseract` if available) | Past papers and course policies are often scans |
| PPTX | `python-pptx` text + tables per slide; **also** convert to PDF via LibreOffice (`soffice --headless --convert-to pdf`) and render image-only slides | Many key slides (charts, case tables, framework figures) carry no extractable text |
| DOCX | `pandoc -t markdown` | Tables come out as CSV-like text; ASCII diagrams in drafts get replaced later |
| XLSX / CSV | pandas / csv | Units and number formats |
| Images | read directly | Hand-written notes, whiteboard photos |
| EPUB / large textbooks | extract per chapter; read only the chapters mapped to the scope | Don't drown in the whole book |

## Image-only slides
`scripts/ingest.py` lists slides with fewer than ~8 words of text. Convert the deck to PDF, render those pages, and **tile 4 per image** (2×2 grid at ~70 dpi) to read them efficiently. Typical hidden content: investment charts, framework figures (e.g. a 2×2 matrix), case-study bullet boxes, worked calculations, timelines.

## Textbooks
Use the textbook to confirm definitions, framework names and canonical numbers. Map chapters to units from the syllabus. Large textbooks: search for the framework names and figures cited in slides rather than reading cover to cover.

## Course policy / syllabus
Extract: unit list and hours, course outcomes, evaluation scheme (internal vs term-end, marks, duration), textbook and references, and anything about exam format. Hours per unit are a proxy for weight when no other signal exists.

## User draft
Convert to markdown and keep it as `workdir/draft.md`. Note its structure, its ASCII diagrams (to be replaced) and every number (to be verified).
