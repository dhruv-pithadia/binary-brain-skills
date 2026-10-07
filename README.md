# Binary Brain Skills

Practical agent skills for Claude Code and Codex, maintained as one shared collection.

## Skills

| Skill | Purpose |
| --- | --- |
| [Mockups](skills/mockups/SKILL.md) | Create interactive HTML prototypes grounded in a project's design language, with UI states, responsive rendering and accessibility audits. |
| [Session Summarizer](skills/session-summarizer/SKILL.md) | Maintain compact, durable project handoffs and finalize documentation on an existing task PR. |
| [Project Initializer](skills/project-initializer/SKILL.md) | Establish shared project instructions, verified setup commands and a compact current-state handoff. |
| [Parallel Execution Planner](skills/parallel-execution-planner/SKILL.md) | Turn an implementation plan into dependency-ordered waves and self-contained agent prompts. |
| [Performance Optimization](skills/performance-optimization/SKILL.md) | Measure bottlenecks, improve frontend, backend and agent performance, and verify the result. |
| [Observability and Instrumentation](skills/observability-and-instrumentation/SKILL.md) | Add structured logs, metrics, tracing, alerts and LLM workflow telemetry. |
| [Security and Hardening](skills/security-and-hardening/SKILL.md) | Apply threat modeling and practical application, agent and deployment safeguards. |

## One source for both agents

Each skill has exactly one canonical folder under `skills/`, with a required `SKILL.md` and only the supporting resources it needs. Shared instructions use tool-neutral language. Optional `agents/openai.yaml` files provide Codex UI metadata without duplicating the workflow.

```text
skills/<skill-name>/
  SKILL.md
  references/          When supporting instructions are needed
  scripts/             When deterministic helpers are needed
  agents/openai.yaml   Optional Codex metadata
```

Existing Claude, Codex and shared copies were reconciled into this collection. Older versions, packaged skill archives and third-party installed skills are excluded. The entrypoints hold shared decision rules; stack-specific examples and PR publication details live in selectively loaded references.

## Local use

Clone this repository to a stable location and keep the checkout available. This repository does not install itself, create symlinks or change agent configuration. Installation into agent discovery folders is a separate, explicit step.

Ask your agent to read the chosen `skills/<skill-name>/SKILL.md` to try a skill directly. Keep its supporting resources together. The mockup renderer requires Node.js 22+ and Chrome or Chromium; set `CHROME_PATH` when the browser is outside its default locations.

## Validation

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python tests/engineering_examples.py
npm ci
node --check skills/mockups/scripts/audit.js
node --check skills/mockups/scripts/states.js
node --check skills/mockups/scripts/run.mjs
REQUIRE_CHROME=1 npm test
```

CI runs structure, reference, JavaScript syntax, executable metric/schema examples and headless Chrome renderer regression checks. The renderer exits 1 on audit/script errors or incomplete screenshots, and 2 on invocation/rendering failures. Warnings require manual judgment, particularly keyboard focus and WCAG target-size exceptions. These checks do not establish that every example works on every stack or that skill behavior has been evaluated across both agents.
