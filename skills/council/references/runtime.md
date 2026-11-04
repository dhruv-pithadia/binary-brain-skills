# Host and T3 execution

Use the current host's tools, authorization, repository instructions, and assigned checkout. A skill does not grant permission to merge, deploy, publish unrelated material, or message others.

## T3

- Resolve models and supported options with `orchestrator_capabilities` once before the first `delegate_task`. Honor explicitly requested versions. Otherwise choose available reviewers suitable for the task and report the selection. Follow the host's native-versus-delegate routing. Each new independent review round is a fresh task with the full brief and findings. Follow returned `next`; do not poll delegates or send reviews through thread messages. Cancel abandoned tasks.
- Review children are read-only and must not publish, start children, or watch PRs. The parent owns integration, commits, publication, and monitoring.
- After creating, taking over, or pushing to a PR, make `link_pull_request` with the full URL the next tool call. Include every PR in a stack.
- Handle actionable PR work, call `watch_pull_request`, and end the turn. Never use shell polling, Monitor, sleeps, or the fallback watcher for a live T3 PR wait. Unwatch before final handoff or a question.
- Search history within the current project, read selected threads before relying on them, and cite returned links verbatim. Do not scan unrelated project transcripts.
- Browser and device work follow the host's current rules. Do not start preview verification unless the request authorizes browser work. When permitted, use `preview_status` first. Use device tools and their returned command for device interaction.

Outside T3, use available native tools without claiming T3 capabilities or independent reviews that did not run. Missing access is an evidence gap. Keep external writes within the user's grant. Resolve companion skills through the host catalog or sibling folders and report required missing capabilities. Use structured arguments or a body file for published text.
