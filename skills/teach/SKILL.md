---
name: teach
description: Explain a subsystem, change, or technical idea plainly at the requested depth, using verified mechanisms and evidence for historical rationale.
---

# Teach

Read [host execution](references/runtime.md). Help the reader understand the requested topic. An explanation request does not authorize changing the product.

Infer the audience, purpose, and existing knowledge from the conversation. Choose the few things they need to understand. Match the requested depth: give a complete one-shot explanation when asked, or a short first layer for an ongoing conversation. Do not force pauses, quizzes, or a full research sweep.

For code, inspect the actual entry points, ownership, data flow, callers, and observable behavior. Trace one concrete example from trigger to result. Explain the mechanism with familiar words and stable names; a list of functions is not an explanation.

Use sibling `why` only when historical rationale matters and is not already established. Keep that investigation scoped. Distinguish what the code does from documented intent, inference, or a plausible explanation. Preserve confidence language when simplifying.

Choose a visual only when it makes the mechanism clearer. One diagram may be enough. Build diagrams progressively when that improves learning, rather than redrawing every three-part flow by rule. Prefer precise editable diagrams for structure and host-permitted images for genuinely spatial evidence. Image generation is optional, not a teaching requirement. Follow T3's visual presentation rules when showing a requested visual.

Lead with a plain definition or the main answer, then develop the explanation in the order the reader needs. State the concrete problem, mechanism, and consequence. Use examples and exceptions that affect understanding; avoid performance framing, canned labels, and unnecessary jargon.

Stop when the requested question is answered. Offer deeper detail only when useful. Report evidence limits without replacing the explanation with a report about the research process.
