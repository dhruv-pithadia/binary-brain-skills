# LLM and agent telemetry

Use a provider adapter rather than assuming every SDK returns `choices[0]` or a `complete` method. Read usage from the installed provider's documented response/stream events; do not estimate tokens using word counts. Track failed/retried attempts as well as successful calls. Missing usage is unknown, not zero. Costs are estimates based on the actual model, cached/input/output categories, pricing version, and currency; token counts alone do not establish billed cost.

For Python `prometheus-client`, this consistent schema separates cumulative tokens/cost from latency:

```python
from prometheus_client import Counter, Histogram

LLM_CALLS = Counter("llm_calls_total", "LLM attempts", ["model", "purpose", "outcome"])
LLM_TOKENS = Counter("llm_tokens_total", "Reported LLM tokens", ["model", "purpose", "token_type"])
LLM_COST = Counter("llm_cost_usd_total", "Estimated LLM cost", ["model", "purpose"])
LLM_DURATION = Histogram("llm_call_duration_seconds", "LLM attempt duration", ["model", "purpose"])
AGENT_RUNS = Counter("agent_runs_total", "Terminal agent runs", ["outcome"])
AGENT_DURATION = Histogram("agent_run_duration_seconds", "Agent run duration", ["outcome"])
AGENT_ITERATIONS = Histogram("agent_iterations_per_run", "Steps per run")
AGENT_TOOLS = Counter("agent_tool_calls_total", "Agent tool attempts", ["tool", "outcome"])
```

All label values must come from configured bounded sets, including purpose, model aliases, registered tool names, and outcomes. Put run IDs in logs/traces only. Suppress automatic content/exception recording that could capture prompts or tool arguments.

Adapter-neutral recording, after a provider response is normalized:

```python
def record_usage(model, purpose, input_tokens, output_tokens, estimated_cost_usd):
    # None means provider did not report this value.
    for token_type, count in (("input", input_tokens), ("output", output_tokens)):
        if count is not None:
            LLM_TOKENS.labels(model, purpose, token_type).inc(count)
    if estimated_cost_usd is not None:
        LLM_COST.labels(model, purpose).inc(estimated_cost_usd)
```

Treat cache/reasoning token breakdowns according to provider semantics: do not add subsets again to the input/output totals. Emit a safe structured event with model alias, purpose, latency, outcome, reported counts, and pricing version; no prompt, task preview, response, tool arguments, or exception text. A truncated task can still contain a complete secret.

## Run accounting and limits

For each run, maintain an accumulator updated with the normalized usage of **every attempt**, including retries. Record known totals plus a completeness flag when any usage/cost is missing; never initialize totals to zero and log them without updating them. Avoid shared mutable global accounting across concurrent runs.

Increment iterations after each attempted step. Record each attempted tool call exactly once, with a bounded outcome. Compare progress/state and repeated normalized actions to diagnose loops; repeated tool names alone do not prove a loop. Apply the application's configured iteration, elapsed-time, and cost/token budgets before further work. A post-call cost check cannot guarantee a hard cap: reserve a bounded next-call budget when the product needs one.

Use a terminal `finally` path to record duration, iterations, and exactly one run outcome (`complete`, `error`, `cancelled`, `iteration_limit`, `time_limit`, or `cost_limit`). Re-raise errors/cancellation after recording; telemetry failure must not replace the application's original error. Test simultaneous runs and cancellation, not just a successful completion.

Sources: [Python labels](https://prometheus.github.io/client_python/instrumenting/labels/), [OpenTelemetry GenAI conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/). GenAI conventions evolve; check the instrumentation's supported schema rather than mixing versions.
