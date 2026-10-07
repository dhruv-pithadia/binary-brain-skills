---
name: parallel-execution-planner
description: Turn a written implementation plan into dependency-ordered execution waves and self-contained agent prompts. Use for planning parallel implementation, not for implementing the feature itself.
---

# Parallel Execution Planner

Produce a saved execution document that a fresh orchestrator can use without reading the conversation. Preserve task boundaries and make dependencies, ownership, integration checks and runtime capacity explicit. Do not implement or dispatch agents as part of planning alone.

## Establish inputs and destination

Read the supplied plan in full. If no path is supplied, use an unambiguous current plan or ask for it. Inspect the repository only enough to resolve concrete paths, commands and conventions.

Use the user's output destination or the repository's existing prompt-document convention. If neither exists, save beside the source plan as `<plan-stem>-agent-prompts.md`. The `docs/superpowers/` layout is an example convention, not a requirement. Mark assumptions that affect execution.

## Extract tasks and shared resources

For each task record its ID, purpose, exact files, tests, inputs, outputs and dependencies. Include shared mutable resources as well as files: development ports, services, test databases, fixtures, external accounts, generated outputs and Git index/branch operations. Disjoint files alone do not establish safe parallelism.

Define dependencies from:

- **Files:** agents cannot concurrently edit the same file. Merge ownership or serialize tasks.
- **Contracts:** consumers follow the task creating their schema, API, types or other inputs.
- **Resources:** isolate mutable services/data/ports or serialize access.
- **Integration:** cross-component tests follow the implementation under test.

Record a task-to-blockers graph. A cycle means the plan needs a joint sequential owner or a revised contract; explain the resolution instead of silently ignoring the dependency.

## Form execution waves

Place tasks with no unresolved blockers in the first wave, remove them, and repeat. Within each wave enforce exclusive file and mutable-resource ownership.

Respect the selected runtime's available agent slots, tool restrictions and the user's concurrency limits. Include the orchestrator in slot accounting when relevant. Do not hardcode an agent count. If capacity is unknown, provide logical waves with a serial fallback and instruct the orchestrator to schedule only as many owners as it can safely run.

Split a large task only when the parts have clear ownership and handoff contracts. Shared-resource setup belongs to one owner before its consumers begin.

## Write the execution document

Add a `Copy Index` with `Copy ID`, `Prompt`, `Wave` and `Purpose`. Use stable IDs such as `ORCHESTRATOR`, `A1`, `A2`. Wrap each copyable prompt in a four-backtick fence, so embedded command fences remain valid, with matching `COPY START: <ID>` and `COPY END: <ID>` markers.

### Orchestrator prompt

Include:

- Objective, source plan and execution authorization boundaries.
- Verified stack, commands, key paths, conventions and critical existing surfaces.
- Runtime capacity assumptions and wave scheduling rules.
- Wave/task ownership, blockers, shared-resource isolation and integration checks.
- Checkout and branch ownership. Reuse a user/runtime-assigned task worktree; otherwise follow repository workflow. Do not switch another thread's branch or edit its checkout.
- Commit ownership. In a shared checkout, only the orchestrator stages/commits after workers finish unless coordinated exclusive Git-index access is established. Alternatively assign separate worktrees and explain how their commits integrate. Independent PR tasks need explicit bases and dependencies.
- Stop conditions: a failed contract/check blocks dependent waves; workers report uncertainty or ownership conflicts before expanding scope.
- Cleanup ownership: stop only task-owned processes and retain valuable work; worktree or branch removal follows explicit cleanup authorization.

### Worker prompts

Each prompt contains its own relevant codebase facts, exact task IDs, permitted files/resources, required reads, implementation steps, test commands and expected evidence. Include what already exists and what must not be changed. State the assigned checkout, branch, port/data isolation and whether the worker may commit.

Tell workers they are not alone, must accommodate other owners' changes, and must not revert them. Define the outputs handed to the next wave, unresolved assumptions and concrete done criteria. Do not rely on inherited conversation context or vague placeholders.

## Validate and save

Check that:

- Every source task belongs to exactly one owner/wave.
- Every dependency is satisfied before its consumer starts.
- Same-wave agents have no overlapping files or unisolated mutable resources.
- Runtime capacity and Git ownership are explicit.
- Every prompt is self-contained, with matching copy markers and valid fences.
- Integration checks cover changed contracts and there is a clear response to failure.

Resolve vague commands or paths before saving. If needed information cannot be established, name it as an execution prerequisite instead of inventing it. Preserve the repository's publication rules: save and report the path; commit/push only when already authorized by the task.
