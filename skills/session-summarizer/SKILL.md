---
name: session-summarizer
description: Maintain a compact, durable project handoff when the user asks to save session knowledge, update context for the next chat, finalize an existing PR's handoff before merging, or consolidate an oversized context file. A conversational recap alone does not require file changes.
---

# Session Summarizer

Make the next session ready to act without rereading the chat. Accumulate validated knowledge, not repeated session narratives. Preserve unfinished work, decision rationale, and evidence limits while keeping startup context small.

## Choose the smallest useful update

Read the project's current handoff and applicable instruction-file conventions. Inspect available conversation history; do not imply access to unavailable history. A request to save or update context authorizes routine consolidation, not implementation, commits, deployments, or changes to permissions. An open PR alone does not select publication mode.

Use existing file locations and structures. Normally `context.md` is the current-state handoff. A short in-chat recap needs no files unless persistence is requested or clearly part of the established wrap-up workflow. Reconcile a stale or contradictory handoff even when the session adds no facts. Make no edit only when there is no material delta and the existing handoff is coherent, current, and appropriately sized. Do not create empty templates or timestamp-only churn.

## Reconcile before writing

- Keep the current objective, active worktree/branch, unfinished work, explicit constraints, implemented behavior, outstanding acceptance, next action, and prerequisites.
- Merge repeated facts and resolve superseded plans in place. A user's explicit decision supersedes an older preference.
- Preserve durable mechanisms, non-obvious failure causes, decision rationale, and important boundaries with their scope and evidence. A temporary failure is not a universal prohibition.
- Move detailed investigations, commands, benchmarks, and historical rationale to an existing runbook, decision record, or progress ledger; link the exact file or section.
- Drop resolved to-dos, abandoned alternatives without ongoing consequences, stale process details, repetitive test logs, and speculation that does not affect upcoming work. Keep a short rejection rationale if it prevents repeating a costly mistake.

Distinguish proposed, implemented, tested, user-accepted, committed/pushed, PR-open, merged, closed-unmerged, and deployed. A test result only supports what it actually covered. Attribute historical results to their date and scope. Mark uncertainty and evidence limits, including who must decide or what is missing. A working implementation does not establish acceptance or deployment, and observed results do not grant new permissions. Refresh volatile details with a small relevant read-only check or mark them last-known; do not start servers, tests or remote audits for an ordinary summary.

## Put knowledge in the right place

| Destination | Contents |
| --- | --- |
| Current handoff, usually `context.md` | Brief current state, active work, constraints, blockers, next step, and pointers |
| Existing topic docs or progress ledger | Reusable findings, evidence, detailed decisions, and remaining work |
| Canonical instruction file or runbook | Newly established project guidance or reusable commands, when authorized |
| Archive, only when needed | Recoverable history removed during substantial consolidation |

Follow project ownership rules. If `AGENTS.md` is canonical and `CLAUDE.md` redirects to it, preserve that arrangement. Do not mirror content unless the project explicitly maintains a mirror. Do not recursively read archives at every wrap-up or add a new startup-reading requirement.

Aim for 600-1,200 words in `context.md` when that suits the project; smaller is better for small projects. Around 1,500 words, consolidate repetition and move detail to linked topic docs. These are editorial targets, not deletion limits. Preserve critical constraints and unresolved work, and honor a project or user budget instead. Re-read the whole edited handoff for contradictions and repetition. A second pass with the same evidence should not materially change or grow it.

## Write and verify safely

Before a substantial rewrite that removes unique history, ensure the exact pre-edit version is recoverable from a verified tracked revision or one local archive copy. Reuse an identical backup; do not accumulate full backups on every wrap-up. Review large handoffs in bounded sections and preserve unreviewed history; truncated tool output is not a complete review. Leave generated and unrelated files alone. Exclude credentials, tokens, raw customer records, and unnecessary personal data; point to private evidence by location.

Inspect the diff and check that active work, explicit deferrals, permissions, and acceptance limits survived; superseded plans are no longer actionable; unrelated work remains intact; links resolve; canonical instructions are not duplicated; and the size is appropriate. Report changed files, what was consolidated or preserved, the next action, and any limits. Do not promise automatic cross-chat memory: continuity depends on the next session reading the saved handoff from an up-to-date checkout.

Use [PR handoff mode](references/pr-handoff.md) only when the user asks to finalize or publish the handoff on an existing task PR, or an established workflow explicitly authorizes it. That reference adds branch, publication, and CI checks; read it before acting in that mode. For an ordinary summary, stop after the checks above.
