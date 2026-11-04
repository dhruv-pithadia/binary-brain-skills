---
name: file-pr
description: Create or update a concise pull request for an authorized task, with validation evidence and an appropriate draft state.
---

# File PR

Read [host execution](references/runtime.md). Verify the assigned checkout/branch, actual remote base, task-owned diff, untracked files, and whether this branch already has a PR. Preserve unrelated work.

Follow repository title conventions. Explain the user-facing problem and resulting behavior, then validation and material limitations. Use measured outcomes only with evidence. Keep implementation inventories, raw review logs, and unsupported percentages out of the description.

Choose draft status from actual readiness and repository policy. Use a draft for incomplete validation or known blockers and state the reason. Open ready for review when the change is coherent and required pre-review checks passed. Bot execution alone is not a reason to label unfinished work ready.

Model attribution is optional unless requested by the user or repository. Use verified public model/harness names if included. Never guess identity or add agent co-authors to commits.

Inspect published text and attachments for secrets and unnecessary private detail. Use structured arguments or a body file. The REST PR endpoint can be a fallback when GraphQL is unavailable, preserving the same scope and draft policy.

In T3 link a created PR or a pushed PR as the next tool call. If monitoring was requested or task work awaits checks, continue with `babysit-pr`. Otherwise hand back the PR, checks, readiness/draft state, and limits. Do not merge or enable auto-merge without an explicit request. Avoid filler comments.
