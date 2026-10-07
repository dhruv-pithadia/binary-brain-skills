---
name: session-summarizer
description: Maintain a compact, durable project handoff when the user asks to save session knowledge, update context for the next chat, finalize an existing PR's handoff before merging, or consolidate an oversized context file. A conversational recap alone does not require file changes.
---

# Session Summarizer

Make the next session ready to act without rereading the chat. Accumulate validated knowledge, not repeated session narratives. Preserve unfinished work, decision rationale and evidence limits while keeping startup context small.

## Choose the smallest useful update

Read the project's current handoff and applicable instruction-file conventions. Inspect the available conversation for new facts; do not imply access to unavailable history. An ordinary request to save or update context authorizes routine consolidation of those notes, not implementation, commits, deployments or changes to project permissions. Use the PR handoff mode below only when the user requests finalizing or publishing the handoff on the existing PR, or an established workflow explicitly authorizes it. An open PR alone does not select that mode.

Use existing file locations and structures. Normally `context.md` is the current-state handoff. A short in-chat recap needs no files unless persistence is requested or clearly part of the established wrap-up workflow. A stale or contradictory handoff needs consolidation even when the session adds no facts. Make no edit only when there is no material delta AND the existing handoff is already coherent, current and appropriately sized. Do not create empty templates or timestamp-only churn.

## Reconcile before writing

Compare existing knowledge with the session delta:

- **Keep:** current objective, active worktree/branch, unfinished work, explicit constraints, implemented behavior, outstanding acceptance, next action and prerequisites.
- **Merge:** repeated facts, updated status and refinements to the same decision. Resolve a superseded instruction in place instead of adding another “latest” block.
- **Retain durable learning:** a reusable mechanism, non-obvious failure cause, decision rationale or important boundary. Include its scope and evidence; a temporary environment failure is not a universal prohibition.
- **Move out of startup context:** detailed investigations, commands, benchmarks and historical rationale already maintained in a runbook, decision record or progress ledger. Link the exact relevant file/section.
- **Drop from active context:** resolved to-dos, abandoned alternatives with no continuing consequence, stale process IDs/ports/results, repetitive test logs and speculative ideas that do not affect upcoming work. Preserve a short rejection rationale if it prevents repeating a costly mistake.

An explicit user decision supersedes an older preference. An observed result can update implementation status but does not grant authority or prove acceptance. Label disagreements and uncertainty when available evidence cannot settle them. Preserve who must decide and what evidence is missing.

Distinguish proposed, implemented, tested, user-accepted, committed/pushed, PR-open, merged into the target branch, closed-unmerged and deployed. Record what a test actually covered and remaining limits, not a blanket “done.” Attribute historical results to their date/scope. Verify volatile details with a small read-only check when relevant, otherwise mark them last-known; do not run servers, tests or remote audits just to refresh an ordinary summary. PR handoff mode additionally requires publication checks as described below.

## Finalize an existing PR's handoff

Run this mode in the original task thread before the user merges. Capture the resulting behavior, non-obvious decisions and rationale, validation evidence, explicit deferrals and remaining work using the shared consolidation rules below.

1. Verify the current task worktree, branch, associated open PR and actual target branch. Reuse them; do not create another worktree or PR. If the PR is missing, already closed or merged, or belongs to another task, report the mismatch without publishing to it. Register the PR with the thread when T3 PR-linking tools are available.
2. Fetch the target branch and compare its latest handoff with the task's version and their common ancestor. Preserve other tasks' knowledge and reconcile superseded facts even when Git reports no textual conflict. Follow the project's branch-update policy if integration is needed; do not overwrite unrelated changes or force-push as part of summarization. Report unresolved semantic conflicts instead of guessing.
3. Update the existing handoff and relevant topic docs in this checkout. Describe implemented behavior without claiming this PR is already merged, accepted or deployed. Identify pending PR work separately from confirmed target-branch state. Treat other threads' activity as last-known unless verified; an open PR does not prove an agent is running. Use durable repository paths and PR links rather than temporary worktree paths as essential references.
4. Inspect the diff, stage only handoff-owned changes, commit and push to the same PR. This mode authorizes those publication steps without repeated confirmation. Do not sweep unrelated staged or working changes into the commit. If no material handoff change is needed, verify that the existing handoff is already published instead of making an empty commit.
5. Run applicable documentation checks and any checks warranted by integration changes. Verify required CI for the latest pushed commit before reporting readiness; do not present earlier code-test results as fresh runs. Address handoff-caused failures within scope and report concrete blockers. Keep remaining acceptance requirements visible.

Finish with the PR link, handoff files changed, publication and check results, and anything the user must still verify. Leave merging to the user; do not enable auto-merge, delete the worktree, or introduce post-merge automation. If the project has no startup instruction to read its handoff, flag that gap without editing instruction files unless authorized.

## Place knowledge where it belongs

| Destination | Contents |
| --- | --- |
| Current handoff, usually `context.md` | Brief current state, active work, key constraints, blockers, next step and pointers |
| Existing topic docs / progress ledger | Reusable findings, evidence, detailed decisions and remaining work |
| Canonical instruction file / runbook | Only newly established project guidance or reusable commands, when the user/task authorizes maintaining it |
| Archive, only when needed | Recoverable historical material removed during substantial consolidation |

Follow the project's ownership rules. If `AGENTS.md` is canonical and `CLAUDE.md` redirects to it, preserve that arrangement. Never mirror content merely because both files exist. Do not turn a one-off session choice into a permanent instruction or add a new startup-reading requirement. Update a mirrored ledger only when the project explicitly maintains that mirror.

Keep durable knowledge cumulative through topic-level updates, not one new document per session. Prefer existing references; create a focused topic note only for unique, useful information that would otherwise be lost. Do not recursively read archives at every wrap-up. When consolidating a large file, inspect its section inventory and relevant sections in bounded reads, track coverage, and do not treat truncated tool output as a complete review. Preserve unreviewed historical content rather than silently discarding it.

## Keep the handoff bounded

Adapt headings to the project. Usually cover: current focus; implementation/workspace state; important decisions; pending checks and next actions; links. Omit empty sections and avoid repeating the full task ledger or runbook.

Aim for **600-1,200 words** in `context.md`; smaller is better for small projects. Around **1,500 words**, consolidate repetition and move detail to linked topic docs. These are editorial targets, not deletion limits: retain critical constraints and unresolved work even when a justified exception is needed. Honor a project/user budget instead when specified. Count words or bytes to detect growth; call a token count an estimate unless measured with a tokenizer.

Re-read the edited whole handoff for contradictory states and repeated facts. A second invocation with the same evidence should not materially change or grow the files. Do not compress by erasing necessary qualifications or producing cryptic fragments.

## Write and verify safely

Routine updates modify relevant sections in place. Before a substantial rewrite that removes unique history, ensure an exact pre-edit version is recoverable: a verified tracked revision containing that version, or one local archive copy. A Git repository alone does not protect uncommitted notes. Reuse an identical existing backup; do not accumulate full backups on every wrap-up. Leave generated or unrelated files alone.

Exclude credentials, tokens, raw customer records and unnecessary personal data. Point to private evidence by location rather than copying it into routinely loaded context.

After writing, inspect the diff and check:

- Active work, explicit deferrals, permissions and acceptance limitations survived.
- Superseded plans no longer appear actionable; unrelated project lanes remain intact.
- New links resolve, referenced knowledge remains recoverable, and canonical instruction files are not duplicated.
- Size is appropriate; no duplicate history or mandatory startup archive reading was introduced.

For ordinary summaries, stop once those checks pass. In PR handoff mode, complete the publication and latest-commit checks above as well. Report which files changed, what was consolidated or preserved, and the next action. For a cleanup, include before/after size and archive location. Do not promise automatic cross-chat memory; continuity depends on the next session reading the saved handoff from an up-to-date checkout.
