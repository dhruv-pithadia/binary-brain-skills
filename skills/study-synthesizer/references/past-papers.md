# Past papers: analysis and question bank

Reference output: `assets/examples/reference-question-bank.pdf`.

## 1. Read every paper
- Past papers are often scanned. Render them with `scripts/ingest.py` (or `pdftoppm -r 110 -png`) and **read each page image**. Crop to the question column when papers have wide outcome-tag columns.
- For each paper record: year, exam type (final / re-exam / midterm), marks, duration, structure (compulsory Q1? "attempt any 4 of 6"?), and every question with its marks and any CO / Bloom's-level tags.

## 2. Map and count
- Tag every question with the **unit** it belongs to under the *current* syllabus, or as `later unit`, `India/region-specific`, or `out of syllabus`.
- Group questions into topics and count **how many papers** each topic appears in (papers, not questions, so one paper repeating a topic doesn't inflate it).
- Produce: a horizontal bar chart "topic → papers out of N" (matplotlib), a coverage table (topic · unit · "in your guide?" ✅ Fully / 🟡 Partly / ❌ Not covered · where to answer from), and an "every question, mapped" table per paper with ★ on repeated topics.
- Flag **syllabus drift**: if older papers follow a different syllabus or textbook, say so clearly, but still prepare the frequently repeated topics (examiners reuse favourites).

## 3. Write the answers
Group by unit (Part B), then frequent out-of-scope topics (Part C). For each question:
- **Header:** marks badge · the question (merge near-duplicates across years into one wording) · frequency tag ("★ 3 papers").
- **Answer:** ① one-line definition to open with → ② named framework (drawn as a flow, table, stack or cards) → ③ 4–6 points in plain words → ④ example with a number (local and global where relevant) → ⑤ risks / limits → ⑥ closing line.
- **🧠 Memory hook:** an acronym or phrase.
- **"Also asked as":** variations this answer covers, plus likely new variants.
- Scale to marks: 2–2.5 marks = 2–4 sentences; 5–7 marks = ~150–250 words; 10–14 marks = ~300–450 words with one visual.

## 4. Last-minute kit (Part D)
Top-10 questions ranked by frequency × fit with the exam scope (with section reference and hook) · the universal long-answer template as a flow · a 2-mark one-liner table for every definition that appears in Q1-style short questions.

## 5. Accuracy
Out-of-scope answers (regional regulation, institutions, dates) rely on research rather than course materials: verify dates and figures against official or reputable sources, cite volatile numbers, and avoid precise figures you can't verify (use "over 50 crore" style ranges instead).
