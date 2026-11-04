---
name: sol-loop
description: Run a bounded independent code-review loop when the user requests sol-loop or a focused reviewer pass.
---

# Sol loop

Read [host execution](references/runtime.md). Use one independent reviewer and a finding ledger for a scoped change.

## Scope and reviewer

Inspect the assigned checkout, branch, status, actual base/head, and task-owned diff including untracked files. Preserve unrelated work. State intent, exclusions, covering checks, and unavailable or pre-existing failures.

Honor an explicitly requested model/version. Otherwise prefer an available Codex Sol reviewer, resolving the current catalog rather than pinning a version. Report the selection before dispatch. If no independent route exists, report the blocker instead of claiming independent approval.

Send a self-contained brief: repository, base/head, intent, exclusions, exact diff command, untracked scope, checks, and gaps. Ask the reviewer to inspect callers and return APPROVE or CHANGES, stable IDs, severity, file/line, evidence, credible trigger, and the smallest useful correction. It must not edit, publish, spawn children, or watch PRs. Do not edit scoped files while it runs.

## Evaluate findings

Keep **impact, likelihood, and task scope separate**:

- Blocker: a credible failure with severe impact, such as an authorization bypass, data loss, or incorrect core behavior.
- Should fix: a demonstrated defect with material impact in the assigned scope.
- Nit: an optional style or maintainability suggestion without demonstrated material harm.

A rare trigger does not make a severe failure a nit. Follow exceptional inputs and adjacent callers far enough to establish risk. Report serious out-of-scope findings with their impact and the smallest safe containment or follow-up; do not relabel them or silently rewrite unrelated code.

Validate each claim. Make the smallest robust correction and prove its behavior. Prefer simplification when it solves the problem; add a lock, guard, helper, or test when evidence calls for it. Disagree with concrete evidence. Track IDs, severity, decisions, reasons, and reviewed heads.

## Recheck and finish

Default to three rounds. Extend only with the user's budget or a concrete unresolved high-impact concern, up to five unless otherwise requested. Later rounds receive the original brief, consolidated ledger, same base diff, and changes since last review. Focus on open IDs and changed behavior.

Stop on approval of current behavior with no substantiated concern. Declined nits and prose-only changes need no new round. Timeouts and budget exhaustion are not approvals. After two evidence-backed exchanges on a disputed finding, report both positions and the decision needed.

Push only within existing task authorization after review and covering checks. Report actual model, rounds, findings, verification, head, gaps, and publication state. Record usage only when exposed.
