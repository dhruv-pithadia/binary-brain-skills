---
name: observability-and-instrumentation
description: Add or repair logging, metrics, tracing, and alerts when requested or when missing telemetry prevents diagnosis. Also use for LLM or agent token, cost, and loop instrumentation. Extend the project's existing telemetry stack.
---

# Observability and Instrumentation

## Discover and choose signals

Read repository instructions and inspect dependency manifests, logger initialization, exporters, dashboards, and alert rules. Search source files by filename first with `rg -l`; inspect only relevant code. Do not print `.env` values, credentials, process environments, or secret-bearing URLs. If configuration discovery is necessary, report variable names and whether they are set, not values.

Reuse existing libraries, conventions, and backends. Add infrastructure only when the requested diagnosis needs it. Define the operational questions first: success rate, latency distribution, failure boundary, queue age, or agent progress and spend. Map each new signal to one of these questions and a likely investigation.

## Instrument the relevant boundaries

- Logs: use stable structured events and safe typed fields. Preserve the existing severity policy. Correlate requests, jobs, and dependency calls; validate incoming correlation IDs for type, length, and allowed characters before propagation. Do not record bodies, credentials, raw query strings, prompts, responses, task previews, or exception messages that may contain them. Error names alone can also be unbounded; normalize them to a small taxonomy.
- Metrics: counters for accumulated events/tokens/cost; histograms for duration and iteration distributions; gauges for current state. Use monotonic elapsed time. Include failures, cancellation, and timeout paths. Normalize route templates and use bounded labels; keep user IDs and run IDs out of labels. Ensure the numerator and denominator describe the same population.
- Traces: propagate existing trace context through HTTP, queue, and async boundaries. Add spans where they explain otherwise invisible work. End spans in failure paths. Redact exception attributes as carefully as logs; automatic instrumentation may capture URLs or arguments.
- Alerts: extend the existing routing and severity conventions. Use user-visible symptoms, meaningful traffic floors, sustained windows, an owner, and a runbook. Thresholds come from an SLO or observed baseline, not from an example.

Read only the relevant supporting reference:

- [Runtime patterns](references/runtime-patterns.md) for Node request context, Python context cleanup, or Rust async spans.
- [Metrics and alerts](references/metrics-and-alerts.md) for a consistent HTTP counter/histogram and Prometheus rule examples.
- [LLM and agent telemetry](references/llm-agent.md) when provider calls or agent loops are the target.

Check installed library versions against official documentation before adapting examples. References are integration patterns, not universal replacement stacks.

## Verify observable behavior

In a local or authorized staging environment, exercise a successful operation, dependency failure, timeout, and cancellation relevant to the change. Confirm correlation across boundaries, emitted series and units, bounded labels, and complete spans. Send synthetic secret markers and verify telemetry contains none. Check rules with `promtool check rules` and evaluate rate and latency queries against representative traffic; test routing through a sandbox receiver unless a live alert test is authorized.

For agents, verify provider-reported usage, retries, aggregated run totals, and terminal outcomes including budget limits. Report the new diagnostic questions answered, validation evidence, and any untested exporters or receivers. Do not send external notifications or change production infrastructure beyond the user's authorized scope.
