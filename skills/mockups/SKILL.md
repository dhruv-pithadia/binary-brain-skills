---
name: mockups
description: Use when the user wants to see how a feature, screen, flow or UI change will look and behave before it is built, asks for a mockup, prototype, wireframe or UI exploration, or says "use the mockups skill".
---

# Mockups

Produce a mockup that shows how the feature will **work for the person using it** and **look like it belongs to this project**. Looks serve the experience, and the project supplies the look.

Request: use the user's skill invocation arguments or infer the request from the conversation.

## Principles

- **Decide from evidence.** Every visual and interaction choice traces to a project fact, a user need, or researched precedent. A choice that traces to nothing is a default, so decide it on purpose.
- **Structure before surface.** Settle what the user does and sees in plain words before touching color, type or polish.
- **Show alternatives.** Compare structural answers when a consequential choice is unresolved.
- **Complete beats pretty.** Cover the relevant states, real content and working interactions for the requested flow.
- **Prove it.** Render it, interact with it, run the audit. Looking at code is not verification.

## Flow

Read each reference when you reach its step, not before. `references/` and `scripts/` sit beside this file; `<skill-dir>` means this file's directory.

1. **Ground** - `references/ground.md`. Read the live project. Separate what must match from what is open.
2. **Frame** - `references/frame.md`. Ask the user as many questions as the answer is worth. Write a short brief with assumptions and get it confirmed.
3. **Research** - `references/research.md`. When the triggers there apply, use the available web search and page retrieval tools; if those are unavailable, say so in the hand off.
4. **Diverge** - `references/diverge.md`. Compare useful alternatives when a consequential structural choice is unresolved; otherwise build the supported recommendation.
5. **Build** - `references/build.md`. One self-contained HTML file in the project's own design language.
6. **Verify** - `references/verify.md`. Render, interact, audit, fix, one critique cycle.
7. **Hand off.** Path, decisions with reasons, the other options with trade-offs, identity directions considered (greenfield), assumptions to confirm, what is mocked, open questions.

**Shortcut:** if the user says "just show me", skip 4 and build your recommended option, stating that you did. Keep project grounding, explicit assumptions, building, verification and handoff proportionate to the change.

**No user to ask** (non-interactive run): list assumptions in the brief, compare alternatives only when they affect a consequential decision, build the recommended approach and disclose unresolved assumptions.

## Output

`.mockups/<feature-slug>/index.html` in the project root. Tell the user once that `.mockups/` may belong in `.gitignore`. Add `options.html` only when the options differ spatially (see `references/diverge.md`). Open it for the user with the T3 preview tools when present, otherwise `open <file>`.
