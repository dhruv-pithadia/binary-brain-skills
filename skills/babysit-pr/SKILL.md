---
name: babysit-pr
description: Monitor a pull request, handle actionable review and CI feedback, and report readiness when asked to watch or babysit it.
---

# Babysit PR

Read [host execution](references/runtime.md). Inspect current head, actual base, checks, human reviews, draft state, unresolved threads, and automatic-merge settings before waiting.

## Observe and act

Use one watcher per PR, owned by the parent task. In T3 handle actionable work, call `watch_pull_request`, and end the turn. Children never watch. Unwatch before final handoff or a question. A wake is evidence to inspect, not a merge decision. Follow host guidance on rate-limit errors; do not retry in a tight loop.

Outside T3, when host rules permit, use the bundled executable:

```sh
<skill-dir>/scripts/pr-wait <pr> --repo owner/name --until ready
```

`ready` requires successful required CI, completed successful supported review-bot checks, addressed threads and human change requests, required approvals, and a non-draft mergeable PR. It waits for Greptile or Macroscope; use `green` for CI-only observation when neither is installed. `green` never means merge-ready. No reported checks is stated explicitly, not described as tested. Exit 0 means the selected condition was observed or the PR merged; 1 needs action; 2 is bad input or a duplicate watcher. Use one long command or a permitted monitor, never both it and the T3 watcher.

Restart after pushes or actionable exits. It retains state between runs, with a fresh baseline after a long gap. Read existing feedback before its first run. The helper observes GitHub state; it does not authorize an atomic merge.

## Review the latest code

Verify findings against source and behavior. **Earlier unresolved feedback remains relevant after a push until the latest code addresses it.** Deduplicate handled events; do not discard a finding because it predates the latest push.

Fix supported in-scope defects and separate code failures from infrastructure failures. Severity follows impact and credible reachability, including rare security/data-loss failures. Record serious out-of-scope risks without silently expanding the change. Read repository-specific bot rules when cited.

Bot names do not override required repository checks. Failed required checks block readiness. A crashed or cancelled review is not successful. Post replies only when authorized, following `leaving-pr-comments`; resolve only after the response succeeds.

## Check readiness and hand back

Fetch the actual base. Check whether it advanced and whether overlapping changes need integration. Proof and review must cover the latest task commit. Update the task branch when needed without overwriting concurrent work and rerun affected checks.

Call a PR ready only when required checks pass, requested reviews cover current behavior, human change requests and required approvals are satisfied, threads are addressed, and it is non-draft, up to date, and mergeable. Report waiting for approval, blocked, or not verified otherwise. Preserve a draft when validation is incomplete.

Merge only if explicitly requested, with a fresh head/base/readiness check immediately beforehand. Do not enable automatic merging as a monitoring side effect. Report the PR link, head, evidence, and limits without filler waiting messages.
