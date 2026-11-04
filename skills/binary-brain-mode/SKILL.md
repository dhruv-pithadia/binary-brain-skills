---
name: binary-brain-mode
description: "Apply Binary Brain's working conventions when explicitly requested: understand the surrounding system, finish authorized work, and prove the result."
---

# Binary Brain mode

Use this mode for the current task's established preferences. Repository and host instructions remain authoritative. It does not grant permission to publish, merge, deploy, or message others.

## Understand the system

Connect a nontrivial change to the user's actual goal. Inspect surrounding ownership, callers, architecture, and user journey enough to find the underlying problem. Name assumptions that could change the approach. Use `why` when historical intent matters, without turning every task into a full investigation.

Prefer quality, simplicity, robustness, scalability, and maintainability. Broader context informs the solution; it does not authorize unrelated rewrites.

## Finish and prove

Carry authorized work through implementation, relevant verification, and a usable handoff. Resolve routine reversible decisions from evidence. Ask only when a consequential product choice or authorization gap requires the user.

For a bug, reproduce it on the relevant end-user surface before changing code and verify that path afterward. Run the repository's required checks. Assess UI quality when exercising a real screen. Keep evidence for observable behavior; a passing build alone is insufficient.

Use the assigned task worktree and branch. Preserve other tasks' changes. Complete authorized commits, pushes, PR linking, and required CI follow-through. Leave merging to the user unless explicitly requested.

Report outcome, evidence, and remaining limits concisely. Never claim an unrun check or an independent review that did not occur.

## Improve recurring work

Prefer architecture, types, lint, scripts, or a focused behavioral test when they can prevent a recurring failure. Use skills for judgment and workflows that those mechanisms cannot express. Apply only directly relevant improvements within the existing grant. Use `reflect` for session lessons or `automate-me` for requested revisions to this mode.

Do not make one-off workarounds universal, rewrite installed skills silently, or claim persistence without a saved artifact. Use actual available tools and models; no particular terminal wrapper or named model is required.
