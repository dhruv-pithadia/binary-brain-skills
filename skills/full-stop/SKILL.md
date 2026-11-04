---
name: full-stop
description: Complete an explicitly requested task through a verified open PR without merging, including bounded review and CI follow-through.
---

# Full stop

Read [host execution](references/runtime.md). Use sibling `sol-loop`, `file-pr`, `babysit-pr`, and `leaving-pr-comments` as needed. Ordinary emphatic "full stop" is not an invocation.

## Boundary

An explicit workflow request covers this task's implementation, relevant tests, commits, pushes, review fixes, and PR updates under repository rules. It does not grant unrelated production changes, deletion, messages, or closure. Never merge, enable auto-merge, enter a merge queue, push to the default branch, or bypass protection.

Inspect auto-merge and queue membership on the task PR before pushes. Disable them within this no-merge task's grant and report the change. Stop before pushing if automatic merging cannot be prevented. Preserve others' work and use the assigned task checkout; otherwise establish one under repository rules.

## Finish and prove

1. Establish goal, actual base/head, callers, user journey, and acceptance evidence. Reproduce a bug on the relevant surface before fixing it when feasible.
2. Implement the smallest robust correction. Verify the same behavior and required repository checks. Record skipped and pre-existing failures.
3. Run bounded independent `sol-loop` review with an available model unless the user named one. Reviewers must not edit or publish. Missing independent review is a gap, not approval. Assess severe rare cases by impact.
4. Fetch the actual base and integrate when needed without overwriting concurrent work. Use a lease tied to the observed head for authorized history rewrites. Repeat affected proof and review after integration changes.
5. File or update the PR with evidence. Keep it draft when proof, review, or required validation is incomplete. Link it through T3 immediately after creation or push.
6. Handle CI and supported findings with `babysit-pr`. Recheck behavior before pushing. Preserve scope and surface material out-of-scope risks.

## Wait and hand off

In T3 handle actionable work, watch, and end the turn. Reassess the latest head on a wake. Do not run a second shell watcher. Unwatch before final handoff or a question.

Readiness requires proof and review of current behavior, passing required checks, addressed findings and human change requests, required approvals, a non-draft up-to-date mergeable PR, verified newer overlapping base changes, and no automatic merging.

Report ready to merge, waiting for required approval, or blocked with its actual reason. Include PR link, final head, evidence, review, and limits. Leave it open and unmerged; report any state change by someone else accurately. Missing responses, budget exhaustion, and unrun checks are not passes.
