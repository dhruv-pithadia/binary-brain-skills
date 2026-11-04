---
name: recall
description: Reconstruct recent project working context from scoped history and live state when asked to catch up, recall work, or resume across sessions.
---

# Recall

Read [host execution](references/runtime.md). Return a current-state brief that makes the next action clear.

## Scope before searching

Use a supplied state capsule first. Resolve the named topic, project, and time window; default an unspecified recent window to seven days and state it. Honor an explicit all-history request rather than silently truncating it. Never read unrelated project histories.

In T3 search project-scoped threads, read selected threads before relying on them, and use their returned links. Elsewhere use explicitly available workspace history or the current conversation, stating its limits. Do not assume Cursor transcript paths exist.

Search topic matches before reading full histories. For one or two relevant threads, work directly. For a large corpus, split bounded slices among authorized readers only when that improves coverage. Keep raw private transcripts out of published artifacts.

## Reconstruct and verify

Extract goals, decisions, corrections, open work, branches, PRs, tickets, and artifacts with source pointers. Distinguish proposed, implemented, verified, pushed, merged, reverted, closed, and deployed.

Check material claims against live PR/branch/ticket state. Broaden into `why` or connected sources only when changed shared context, a contradiction, or missing evidence could change the next action. Do not launch a full historical investigation for every named feature.

When the answer depends on which tools or files an agent actually used, inspect the relevant activity rather than assuming its final summary proves it. Mark last-known or inaccessible state accurately.

## Brief

Lead with a short capsule of the current objective and state, then concise thread statuses, material recurring problems, and the single most useful next action. Use status labels that match observed reality, including blocked or closed-unmerged when appropriate. Keep adjacent work out unless it blocks the topic.

Link the supporting histories and current artifacts. Keep deeper detail below the brief or omit it. Stop when the requested context is reconstructed; do not implement, publish, or start services from a recall request alone. For a durable saved handoff, use `session-summarizer` when requested.
