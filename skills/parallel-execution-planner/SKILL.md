---
name: parallel-execution-planner
description: Use when turning a written implementation plan into coordinated multi-agent work, wave planning, or self-contained sub-agent prompts from project plans.
---

# Parallel Execution Planner

## Purpose

Turn a written implementation plan into a multi-agent execution prompt document. The output is a saved Markdown prompt that an orchestrator agent can use to dispatch sub-agents wave by wave.

Do not implement the feature while using this skill. Produce the execution prompt document only.

## Inputs

Expected usage:

```text
/parallel-execution-planner docs/superpowers/plans/<date>-<feature>.md
```

If the user gives a plan path, read that full file. If no path is given, ask for the plan path unless there is exactly one obvious current plan in the conversation.

Save output to:

```text
docs/superpowers/prompts/<same-date>-<feature>-agent-prompt.md
```

Use the date and feature slug from the plan filename. For example:

```text
docs/superpowers/plans/2026-06-11-tally-seed-package-import.md
docs/superpowers/prompts/2026-06-11-tally-seed-package-import-agent-prompt.md
```

## Workflow

### 1. Read The Plan

Read the entire implementation plan. Extract each task into a working table:

- Task ID, such as `T1`, `T2`, or the plan's native numbering.
- Task title.
- Exact files created or modified.
- Tests or verification commands mentioned.
- Logical inputs from earlier tasks.
- Outputs this task produces for later tasks, such as schema, API shape, model, parser contract, UI type, or migration.

If the plan omits exact paths, inspect the repo enough to infer concrete paths before writing the prompt. Mark assumptions explicitly in the orchestrator prompt.

### 2. Build The Dependency Graph

Use two dependency types:

- **File conflict:** two tasks create or modify the same exact file. These tasks cannot be assigned to separate same-wave agents. Merge them into one agent or place them in sequential waves.
- **Logical dependency:** Task B consumes an output from Task A. B must follow A even if files do not overlap.

Common logical dependencies:

- Database migration before models, services, or routes that rely on the new table.
- Backend schema/API contract before frontend integration.
- Parser/normalizer output before importer, validator, or UI result rendering.
- Shared types/helpers before callers.
- Tests that assert end-to-end behavior after the components under test exist.

Represent the graph internally as `task -> blockers`.

### 3. Group Into Waves

Build waves with this algorithm:

1. Wave 1 contains all tasks with no unresolved dependencies.
2. Remove Wave 1 from the graph.
3. Wave 2 contains tasks whose blockers are now complete.
4. Repeat until every task is placed.

Apply these constraints:

- No two agents in the same wave may modify the same file.
- Same-wave tasks with file conflicts must be merged into one agent.
- Aim for 2-4 agents per wave.
- If one wave has more than 4 independent tasks, split by ownership area, such as backend, frontend, tests, docs, migrations.
- If a task is too large for one agent, split it only when the split produces independent file ownership and clear handoff contracts.

If the graph has a cycle, identify the cycle, merge the involved tasks into one sequential agent, and explain why in the prompt.

### 4. Write The Prompt Document

Create a Markdown document with two main parts.

Before Part A, add a `Copy Index` table so the user can distinguish and copy each prompt independently. The table must include:

- `Copy ID`
- `Prompt`
- `Wave`
- `Purpose`

Use stable copy IDs:

- `ORCHESTRATOR` for the orchestrator prompt.
- `A1`, `A2`, `A3`, etc. for sub-agent prompts, matching wave/agent naming.

Wrap every copyable prompt in a four-backtick fenced block with explicit copy markers:

`````markdown
````text
COPY START: ORCHESTRATOR

...orchestrator prompt text...

COPY END: ORCHESTRATOR
````
`````

For sub-agents, use the agent copy ID:

`````markdown
````text
COPY START: A1

...sub-agent prompt text...

COPY END: A1
````
`````

Use four backticks for the outer prompt block because the prompt text itself often contains triple-backtick command snippets. This keeps Markdown rendering clean and makes each prompt easy to copy.

#### Part A: Orchestrator Prompt

Include:

- Role statement: the orchestrator coordinates sub-agents and integrates results.
- Source plan path.
- Output branch or repo assumptions if visible.
- Codebase facts: stack, key paths, existing routes/services/components, conventions, test commands, and critical "already exists" warnings.
- Wave execution order.
- For each wave: agent names, task IDs, touched files, dependency notes, and integration checks.
- Rules for the orchestrator:
  - Dispatch only one wave at a time.
  - Wait for all agents in a wave before starting the next wave.
  - Run integration checks between waves when contracts change.
  - Resolve file conflicts manually before continuing.
  - Do not let agents edit files outside their assigned scope unless they report back first.

#### Part B: Sub-Agent Prompts

Write one sub-agent prompt per agent. Each prompt must be fully self-contained and include:

- Role statement.
- Relevant codebase facts subset.
- Assigned task IDs and titles.
- Exact files the agent may create or modify.
- Files the agent should read first.
- Step-by-step implementation instructions from the plan.
- Hard constraints, including what not to touch.
- Test or verification command.
- Commit command for the agent's completed slice, if per-agent commits are intended.
- Done criteria.

Use concrete file paths and commands. Avoid placeholders such as `TODO`, `TBD`, `appropriate`, `similar`, or `etc.` in agent instructions.

### 5. Self-Review Before Saving

Before writing the final file, verify:

- Every task from the source plan appears in exactly one wave.
- Every task appears in exactly one sub-agent prompt.
- No two agents in the same wave modify the same file.
- Wave ordering satisfies all file-conflict and logical dependencies.
- Every sub-agent prompt is self-contained.
- The document includes a `Copy Index`.
- Every copyable prompt has matching `COPY START: <ID>` and `COPY END: <ID>` markers.
- Copyable prompt blocks use four-backtick fences so embedded command snippets render correctly.
- Codebase facts cover non-obvious pitfalls and existing implementation surfaces.
- The prompt document tells the orchestrator when to run tests and how to handle failed checks.

After saving, run a quick text check against the prompt file:

```bash
rg -n "TODO|TBD|placeholder|later|fill in|appropriate|similar to" docs/superpowers/prompts/<filename>.md
```

The check should return no matches unless the words are quoted from the source plan and explicitly called out.

### 6. Commit The Prompt

After the prompt passes self-review:

```bash
git add docs/superpowers/prompts/<filename>.md
git commit -m "docs: parallel execution prompt for <feature>"
```

If the user did not ask for commits in the current session, save the file and report the exact commit commands instead of running them.

## Output Quality Bar

The final prompt should let a fresh orchestrator agent execute the plan without rereading the full conversation. It must preserve task boundaries, make dependencies explicit, and prevent same-wave agents from colliding on files.
