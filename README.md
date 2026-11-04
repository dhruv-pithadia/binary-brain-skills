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
| [Study Synthesizer](skills/study-synthesizer/SKILL.md) | Turn a folder of course materials into an exam-ready visual study guide PDF, with diagrams, cases, mnemonics, model answers and an optional past-paper question bank. |
| [Automate Me](skills/automate-me/SKILL.md) | Capture explicit preferences and scoped recurring evidence in a personal mode. |
| [Babysit PR](skills/babysit-pr/SKILL.md) | Handle review and CI feedback using T3's watcher or a tested fallback outside T3. |
| [Binary Brain Mode](skills/binary-brain-mode/SKILL.md) | Apply explicitly selected conventions for system context, autonomy, and proof. |
| [Council](skills/council/SKILL.md) | Reconcile two independent reviews using available or explicitly requested models. |
| [Demo](skills/demo/SKILL.md) | Create narrated vertical explainers with verified timing and a measured machine budget. |
| [File PR](skills/file-pr/SKILL.md) | Publish a concise task PR with evidence and an appropriate draft state. |
| [Full Stop](skills/full-stop/SKILL.md) | Complete and verify a task through an open PR without merging it. |
| [Leaving PR Comments](skills/leaving-pr-comments/SKILL.md) | Write authorized, evidence-backed replies and verify posting succeeded. |
| [Modernize](skills/modernize/SKILL.md) | Reassess an aging PR's intent before safely rebasing and updating it. |
| [Recall](skills/recall/SKILL.md) | Recover scoped working context and verify it against live state. |
| [Reflect](skills/reflect/SKILL.md) | Identify durable session lessons and suitable structural or skill improvements. |
| [SEO](skills/seo/SKILL.md) | Diagnose search visibility using observed crawl, render, indexing, and performance evidence. |
| [Sharpen](skills/sharpen/SKILL.md) | Deepen a prompt using primary evidence, concrete methods, and independent validation. |
| [Sol Loop](skills/sol-loop/SKILL.md) | Run bounded independent review while separating severity, likelihood, and scope. |
| [Teach](skills/teach/SKILL.md) | Explain verified mechanisms at the requested depth without compulsory research or visuals. |
| [Technical Writing](skills/technical-writing/SKILL.md) | Write precise documentation and valid examples with reader-oriented structure. |
| [Unslop](skills/unslop/SKILL.md) | Audit and polish existing screens while preserving behavior, accessibility, and brand. |

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

## T3 compatibility

The added workflows share one canonical source for Codex and Claude in T3. Their local host references describe model discovery, native/delegate routing, immediate PR linking, parent-owned watches, and project-scoped history. Explicitly requested model versions are honored; default reviewers resolve from the actual catalog. A missing independent route is reported rather than represented as approval.

T3 uses `watch_pull_request` and never the bundled shell watcher for a live PR wait. The fallback `pr-wait` is retained for permitted non-T3 hosts and tested with an isolated GitHub CLI double. Neither watcher grants merge authorization. Review scope includes unresolved feedback that predates a push, and rare severe failures retain their impact-based severity.

`binary-brain-mode` and `sharpen` retain explicit-only invocation metadata. Other workflows use their documented request triggers. Video work requires the available HyperFrames/media skills and providers; importing this collection does not install those dependencies or assume a particular user's hardware. No global discovery folders, symlinks, or agent settings are changed by adding these canonical repository copies.

Attribution and source revision are recorded in [third-party notices](THIRD_PARTY_NOTICES.md). The reference repository remains unchanged.

## Validation

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_skills.py
.venv/bin/python -m unittest discover -s tests -p 'test_*.py' -v
.venv/bin/python tests/engineering_examples.py
npm ci
node --check skills/mockups/scripts/audit.js
node --check skills/mockups/scripts/states.js
node --check skills/mockups/scripts/run.mjs
REQUIRE_CHROME=1 npm test
```

CI runs structure, reference, JavaScript syntax, executable metric/schema examples and headless Chrome renderer regression checks. The renderer exits 1 on audit/script errors or incomplete screenshots, and 2 on invocation/rendering failures. Warnings require manual judgment, particularly keyboard focus and WCAG target-size exceptions. These checks do not establish that every example works on every stack or that skill behavior has been evaluated across both agents.

The Python regressions also exercise the fallback PR watcher through its CLI and verify non-destructive audio analysis. [Decision scenarios](tests/skill_scenarios.json) and their [independent evaluation record](tests/skill-evaluation-results.md) cover selected workflow judgments. These simulations do not establish live model routing, hosted watcher delivery, or end-to-end video production. Re-run independent evaluations by giving only each case's skill, request, and context to a fresh evaluator, withholding the required/forbidden rubric until scoring.
