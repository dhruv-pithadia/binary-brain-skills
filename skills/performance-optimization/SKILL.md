---
name: performance-optimization
description: Measure, diagnose, and fix a performance bottleneck across frontend, backend, database, or agent workflows. Use when a slowdown, regression, or performance requirement needs investigation.
---

# Performance Optimization

Find the measured bottleneck, make the smallest change that addresses it, then verify both performance and correctness. Do not optimize from intuition alone.

## Understand the project and symptom

Read the repository's canonical instruction files and current handoff when present. Identify the relevant stack, runtime, deployment shape, and user-visible symptom from the project files and the report. Do not assume that optional files such as `CLAUDE.md` or `context.md` exist.

Make the symptom measurable. Choose a representative workload, environment, data size, and metric before changing code. Examples include route-level LCP/INP, endpoint p95 latency, query duration and rows read, CPU profile samples, memory over time, or model-call latency and tokens. Prefer existing production telemetry or a repeatable local/staging reproduction. Record the baseline and its limits.

Choose a profiler from the stack and symptom: browser performance tools or Lighthouse for page behavior; a CPU/heap profiler for application hot paths; query plans and query telemetry for databases; per-call traces for agent workflows. Use representative builds and workloads. A profile or a timing measurement should identify the cost before a fix is chosen.

## Fix the demonstrated cause

Trace the slow path from the user-visible symptom to the measured cost. Check nearby causes such as repeated database round trips, unbounded reads, avoidable serialization, blocking work, excessive rendering, oversized assets, sequential independent calls, or repeated model context. Treat these as hypotheses to measure, not a checklist of presumed defects.

Choose a fix that preserves behavior and fits the system's concurrency, consistency, memory, and failure requirements. For database indexing, derive column order from the real predicates, ordering, operators, and data types. On common B-tree indexes, equality columns generally lead, followed by the first range column; confirm the engine's rules, including sort direction. Selectivity alone is not a universal ordering rule. Check the candidate against the actual query plan and workload, and weigh write/storage cost.

Pagination must use a deterministic, unique ordering. For keyset pagination, include a unique tie-breaker in both the cursor predicate and `ORDER BY`; a timestamp alone can skip or duplicate rows when timestamps collide. Use a cursor predicate that matches the chosen sort directions and null handling.

For frontend rendering, first inspect whether the project has React Compiler or another compiler/runtime optimization enabled. Then profile the specific interaction. Parent renders can cause child components to render again when no applicable bailout is in place, but a child does not re-render merely because an unrelated sibling rendered. Add manual memoization only when profiling shows a benefit or a stable identity is required for correctness or effect behavior.

For Python async code, `asyncio.to_thread` can keep blocking work from stalling the event loop, especially blocking I/O. It does not generally make pure Python CPU-bound work faster because of the GIL; use an appropriate process pool, native implementation, or library that releases the GIL when parallel CPU execution is needed.

Use conditional stack examples only when they make the chosen fix clearer: [stack-specific examples](references/stack-examples.md).

## Verify the result

Repeat the baseline workload with the same metric, environment, and data shape. Compare before and after values and note variance. Confirm that the profiled cost improved, then check correctness, resource use, and important neighboring paths. Run the relevant tests and inspect traces or plans for regressions.

If the change is not measurably better, or it shifts cost into a worse resource or path, revise or remove it. Record the result and limitations so later work does not mistake a local benchmark for a production guarantee.

Add a regression guard only when a stable signal can be maintained, such as a representative benchmark, query-count assertion, bundle-size check, or service-level alert. Set budgets from the product's workload, user expectations, and service objectives; generic thresholds are examples, not universal acceptance criteria.
