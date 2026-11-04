---
name: council
description: Obtain two independent, evidence-backed reviews of a scoped change or design when the user requests council review.
---

# Council

Read [host execution](references/runtime.md). Publication and merging follow the user's existing authorization.

## Resolve the panel and scope

Record the goal, actual base/head, scoped diff including untracked files, constraints, and covering checks. Give design reviewers the same requirements and raw evidence instead of inventing a diff. Fix known in-scope failures before review.

Honor requested providers, models, reasoning, and budget. Otherwise select two distinct available reviewer models, preferably from different providers, and state the actual panel before dispatch. Resolve catalog IDs and options rather than guessing slugs. If two independent reviewers cannot run, report the limitation; a local pass is not a complete council.

## Review independently

Give both reviewers the same self-contained brief. They must inspect surrounding callers, verify claims, and return APPROVE or CHANGES for the specified head, stable finding IDs, severity, location, evidence, and the smallest credible correction. They must not edit, publish, spawn children, or watch PRs. Do not edit reviewed files while either runs.

Assess severity from impact and credible reachability, separately from scope and frequency. Rare security, data-loss, and concurrency failures can be blockers. Record out-of-scope risks without silently expanding implementation. Scores are optional and never substitute for evidence.

## Reconcile and stop

Verify claims yourself. Fix supported in-scope defects, reject unsupported claims with reasons, and track IDs, decisions, and reviewed heads. Default to three rounds at most. Later rounds inspect changed behavior and open findings with the original scope and consolidated ledger. Prose-only fixes and declined nits need no new round.

Changed behavior needs fresh review coverage. Stop when both approve current behavior and no substantiated concern remains. If a finding remains disputed after two evidence-backed exchanges or the budget ends, report the disagreement and decision needed. Missing responses and timeouts are not approvals.

Report reviewed head, actual models, rounds, accepted and declined findings, checks, and gaps. Update a PR only when authorized. Leave merging to the user unless explicitly requested.
