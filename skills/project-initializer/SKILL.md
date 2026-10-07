---
name: project-initializer
description: Establish project instructions and a compact handoff for a new or existing project. Use when the user asks to initialize project context or onboard a repository; preserve existing instruction-file conventions.
---

# Project Initializer

Make the project understandable to a fresh Claude Code or Codex session. Record verified setup commands, stable project constraints, current state and the next useful action.

## Inspect before writing

Read existing README, instruction files, handoffs, manifests, scripts and relevant architecture notes. Follow applicable repository instructions and use the current task checkout. Do not create another worktree or branch solely for context documentation.

Infer the project purpose, stack, run and test commands, deployment process and configuration requirements from live files. Ask only for missing facts that materially affect the handoff. Mark unverified commands and assumptions instead of inventing them. Describe required environment variables by name and purpose; never copy credentials or private customer data.

## Preserve the project's ownership rules

Use existing paths and file structures. Add missing information without replacing unrelated instructions or changing permissions.

- If `AGENTS.md` is canonical and `CLAUDE.md` redirects to it, preserve that arrangement.
- If the project deliberately mirrors files, maintain its established mirror.
- If it already has a handoff or runbook, update that document rather than creating a competing one.
- Leave generated files untouched.

For a project with no conventions, use this layout:

```text
AGENTS.md       Stable project instructions and reusable commands
CLAUDE.md       Short instruction to read AGENTS.md
context.md      Compact current-state handoff
```

Put the shared instructions in `AGENTS.md`. Keep `CLAUDE.md` minimal:

```markdown
# Project instructions

Read and follow `AGENTS.md` in this directory before starting work.
```

Do not claim that this redirect syntax gives automatic cross-chat memory. It is an instruction to the agent; continuity depends on reading these files from an up-to-date checkout.

## Write stable instructions

Include only useful, established information:

- Project purpose and major components.
- Stack and relevant repository conventions.
- Exact development, test, lint and build commands, with their working directories.
- Environment setup and reusable operational guidance.
- Existing safety boundaries and ownership rules.
- A short instruction to read the current handoff at session start, when initializing a new context system.

Do not introduce blanket approval requirements for dependencies, schema changes or ordinary work. Preserve the user's and repository's actual rules. Do not make a one-session choice into a permanent constraint.

## Write a compact handoff

Use `context.md` when no other handoff is established. Adapt headings to the project and omit empty sections. Cover:

- Current objective and what already works.
- Important architecture and durable decisions, with rationale.
- Active work, explicit deferrals and known blockers.
- Validation evidence, its limits and any commands not yet verified.
- Next action and prerequisites.
- Links to existing topic docs or runbooks for detail.

Aim for a small current-state document, usually 600-1,200 words or less. Update facts in place rather than appending an ever-growing session history. Keep detailed investigations in existing topic documents and link them. Preserve unresolved work and unique historical knowledge when consolidating an existing handoff; ensure removed unique material is recoverable from an exact tracked version or one local archive.

Distinguish proposed, implemented, tested, accepted, committed, PR-open, merged and deployed. A working implementation does not establish user acceptance or deployment.

## Verify and report

Inspect the diff and re-read all changed documents. Check that commands have evidence, local links resolve, established instructions remain intact, no secrets were included and shared guidance is not duplicated. A second initialization with the same facts should not materially grow the files.

Report the files created or updated, assumptions still requiring confirmation and the next useful action. Do not commit or push solely because context files were initialized; follow the current task's publication authorization.
