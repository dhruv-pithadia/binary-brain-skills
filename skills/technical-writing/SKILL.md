---
name: technical-writing
description: Write or review developer documentation, RFCs, readmes, PR descriptions, and commit messages with clear structure and precise, readable language.
---

# Technical writing

Read [host execution](references/runtime.md). Make the text accurate and easy for its intended reader to use.

## Choose structure from the reader's task

Use Diataxis as a guide: tutorials support learning by doing, how-to guides solve a practical task, reference supports lookup, and explanations build understanding. Keep each section focused. Separate long digressions when they obscure the task; a useful table or short explanation can remain inside a procedure. Do not fragment a small document merely to enforce a taxonomy.

- Tutorials produce visible progress and describe expected results.
- How-to guides state prerequisites and actionable steps, with decision points where needed.
- Reference documents describe actual names, options, limits, and errors consistently.
- Explanations connect mechanisms, context, tradeoffs, and rationale.

RFCs and decision records may combine a recommendation, evidence, and reference material. PR bodies briefly explain the problem, resulting behavior, checks, and limits. Follow repository templates and conventions.

## Write precise prose

Use short familiar words, active verbs, and concrete actors. Preserve real symbols, commands, paths, flags, units, and product names. Keep terminology consistent. Remove filler and invented metaphors; explain unfamiliar terms when they are necessary.

Put conditions and consequential warnings before the instruction they qualify. Keep instructions in an intelligible sequence and describe expected outputs. Distinguish required steps from optional choices.

Vary sentence length naturally. Split a sentence when it hides multiple decisions, not at a universal word count. Keep grammatical articles and qualifiers that prevent ambiguity. Place only/not next to what they modify and make pronouns refer to one clear subject. A clarity rule that makes a sentence worse needs judgment, not mechanical enforcement.

Use evidence for factual claims and preserve uncertainty. Do not remove a qualification merely to sound confident. Never invent measured outcomes, user benefits, author intent, or compatibility.

## Format for the actual artifact

Use descriptive links, parallel lists, sentence-case headings, and code formatting for symbols. Use the document's established style. Product UI copy follows the product's copy and localization conventions.

Keep code snippets valid in their language and faithful to the repository. Do not mandate tabs for YAML, Python, or other indentation-sensitive examples. Preserve significant whitespace, quoting, and actual newlines. Test executable examples when relevant and feasible.

Plain-language editing is part of this skill; the UI-only `unslop` skill is not a prose dependency. Avoid unsolicited skill-edit suggestions in the finished document.

## Verify and finish

Check commands, counts, paths, links, examples, and volatile facts against current primary evidence. Distinguish verified facts from last-known state. Inspect the rendered artifact when layout matters and host tools permit it; source inspection alone is not a visual check.

Read the whole result for coherence, repetition, broken references, and changes to meaning. Preserve user decisions and publication boundaries. Return the requested text or saved artifact with concise verification limits.
