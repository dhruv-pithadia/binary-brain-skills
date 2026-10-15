---
name: project-initializer
description: Initialize project-local instructions, product requirements, design, architecture and a current-state handoff for a new or existing project. Use when the user asks to initialize project context or onboard a repository; preserve existing instruction-file conventions.
---

# Project Initializer

Make the project understandable to a fresh Claude Code or Codex session. Create the project documents automatically from the user's brief and available evidence. Record agreed requirements, design and architecture, verified setup commands, current state and the next useful action. Keep generated documents inside the target project, never in global agent configuration or the installed skill directory. Initialization creates documentation; it does not itself scaffold application code or install dependencies.

## Inspect before writing

Read existing README, instruction files, handoffs, manifests, scripts and relevant architecture notes. Follow applicable repository instructions and use the current task checkout. Do not create another worktree or branch solely for context documentation.

For an empty folder, use the current conversation and user brief as the starting evidence. Create every required document even when details are undecided: record what is known, label proposals, and list specific open questions instead of inventing facts or leaving empty boilerplate. A project without a UI still gets `design.md`, noting that visual design is not applicable and recording any relevant CLI or output conventions.

For an existing project, infer its purpose, stack, run and test commands, deployment process and configuration requirements from live files. Ask only for missing facts that materially affect the handoff. Mark unverified commands and assumptions instead of inventing them. Describe required environment variables by name and purpose; never copy credentials or private customer data.

## Preserve the project's ownership rules

Use existing paths and file structures. Add missing information without replacing unrelated instructions or changing permissions.

- If `AGENTS.md` is canonical and `CLAUDE.md` redirects to it, preserve that arrangement.
- If the project deliberately mirrors files, maintain its established mirror.
- If it already has a handoff or runbook, update that document rather than creating a competing one.
- Leave generated files untouched.

For a brand-new project, create all seven files below in the project root in one initialization. Use these exact names when no conventions exist:

```text
README.md
AGENTS.md
CLAUDE.md
prd.md
design.md
architecture.md
context.md
```

For existing projects, reuse equivalent documents and their established casing or paths; add missing coverage without creating duplicate sources of truth.

Put the shared instructions in `AGENTS.md`. Keep `CLAUDE.md` minimal:

```markdown
# Project instructions

Read and follow `AGENTS.md` in this directory before starting work.
```

Do not claim that this redirect syntax gives automatic cross-chat memory. It is an instruction to the agent; continuity depends on reading these files from an up-to-date checkout.

## Populate the project documents

Give each document one job and link to the canonical source instead of copying facts across files:

- `README.md`: concise project overview, setup and run instructions, and links to the project documents. Label planned or unverified commands.
- `prd.md`: problem, target users, goals, scope and exclusions, core user journeys, requirements and acceptance criteria. Separate agreed requirements from proposals and open questions.
- `design.md`: agreed visual direction, typography, colors, spacing, layout, component reuse, responsive behavior, accessibility and interaction states. Reference available assets or existing tokens; do not invent an approved design system. Keep undecided choices explicit.
- `architecture.md`: proposed or implemented stack, component boundaries, data flow, storage, integrations, deployment shape and durable technical decisions with rationale. Distinguish planned structure from files and services that exist.
- `context.md`: current objective, defined and undecided items, implementation and validation status, blockers and the next useful action. Link to requirements, design and architecture rather than repeating them.

In a new empty project, explicitly record that implementation and validation have not started. Do not present documentation creation as application progress.

## Write stable instructions

Include only useful, established information:

- A brief project orientation and relevant repository conventions.
- Exact development, test, lint and build commands, with their working directories, or a link to their canonical setup section.
- Reusable operational guidance that is not already documented elsewhere.
- Existing safety boundaries and ownership rules.
- Compact document routing and maintenance instructions, when initializing a new context system. Use the following block, adapting paths to the project:

```markdown
Read `context.md` at session start; use `README.md` for setup.
Before changing scope, UI or system structure, read `prd.md`, `design.md` or `architecture.md`, respectively.
Keep the relevant document current when its facts or agreed decisions change; update `context.md` at handoff. Link rather than duplicate.
```

Keep this routing to a few lines. Do not paste document summaries, requirements, design tokens or architecture details into `AGENTS.md`, and do not require every document to be read on every task.

Do not introduce blanket approval requirements for dependencies, schema changes or ordinary work. Preserve the user's and repository's actual rules. Do not make a one-session choice into a permanent constraint.

## Write a compact handoff

Use `context.md` when no other handoff is established. Adapt headings to the project and omit empty sections. Cover:

- Current objective and what already works.
- Links to canonical architecture and durable decisions; include rationale here only if it has no established home.
- Active work, explicit deferrals and known blockers.
- Validation evidence, its limits and any commands not yet verified.
- Next action and prerequisites.
- Links to existing topic docs or runbooks for detail.

Aim for a small current-state document, usually 600-1,200 words or less. Update facts in place rather than appending an ever-growing session history. Keep detailed investigations in existing topic documents and link them. Preserve unresolved work and unique historical knowledge when consolidating an existing handoff; ensure removed unique material is recoverable from an exact tracked version or one local archive.

Distinguish proposed, implemented, tested, accepted, committed, PR-open, merged and deployed. A working implementation does not establish user acceptance or deployment.

## Verify and report

Inspect the diff and re-read all changed documents. For a new project, confirm all seven files exist and are populated with known facts or explicit unknowns. Check that the compact routing uses the actual filenames, commands have evidence, local links resolve, established instructions remain intact, no secrets were included and shared guidance is not duplicated. A second initialization with the same facts should not materially grow the files.

Report the files created or updated, assumptions still requiring confirmation and the next useful action. Do not commit or push solely because context files were initialized; follow the current task's publication authorization.
