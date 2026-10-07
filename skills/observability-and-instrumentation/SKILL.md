---
name: observability-and-instrumentation
description: Instruments code so production behavior is visible and diagnosable. Use when adding logging, metrics, tracing, or alerting to any project. Use when shipping any feature that runs in production. Use when a production issue couldn't be diagnosed because the data wasn't there. Use when building or reviewing LLM/agent workflows that need cost tracking, loop detection, and step tracing. Always scans the project first before recommending any tooling - adapts to what exists, never replaces it blindly.
---

# Observability and Instrumentation

Code you can't observe is code you can't operate. Instrumentation is not a post-launch add-on - it's written alongside the feature, the same way tests are. The first production incident with no telemetry is archaeology. The second one is negligence.

---

## Step 0: Scan the Project First

Before writing a single line of instrumentation, understand what already exists. Never prescribe a tool the project hasn't chosen.

```bash
# Detect language and runtime
ls package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
cat package.json 2>/dev/null | grep -E "(winston|pino|bunyan|morgan|opentelemetry|datadog|sentry|prometheus)"
cat pyproject.toml requirements.txt 2>/dev/null | grep -E "(loguru|structlog|logging|opentelemetry|sentry|prometheus|datadog)"
cat Cargo.toml 2>/dev/null | grep -E "(tracing|log|sentry|opentelemetry)"

# Detect existing logging setup
grep -r "logger\|logging\|winston\|pino\|loguru\|structlog\|console\.log" src/ app/ --include="*.ts" --include="*.js" --include="*.py" --include="*.rs" -l 2>/dev/null | head -10

# Detect existing metrics
grep -r "prometheus\|metrics\|counter\|histogram\|gauge" src/ app/ -l 2>/dev/null | head -5

# Detect existing tracing
grep -r "opentelemetry\|jaeger\|zipkin\|datadog\|span\|trace" src/ app/ -l 2>/dev/null | head -5

# Detect existing error tracking
grep -r "sentry\|bugsnag\|rollbar" src/ app/ -l 2>/dev/null | head -5

# Detect if LLM/agent calls exist
grep -r "openai\|anthropic\|langchain\|llm\|agent\|completion" src/ app/ -l 2>/dev/null | head -5

# Check infrastructure
cat docker-compose.yml 2>/dev/null | grep -E "(grafana|prometheus|loki|jaeger|datadog)"
ls .env .env.example 2>/dev/null | xargs grep -i "sentry\|datadog\|newrelic\|honeycomb" 2>/dev/null
```

**Based on what you find, take one of these paths:**

| Situation | Action |
|---|---|
| Logging library exists | Extend it - add structure, correlation IDs, missing log points |
| No logging library | Recommend one appropriate for the stack (see Stack Defaults below) |
| Metrics setup exists | Add RED/USE metrics to new endpoints/services using same library |
| No metrics setup | Present options (see Alerting & Metrics Options below) |
| Tracing exists | Extend with manual spans where needed |
| No tracing | Only add if cross-service or async boundaries exist - don't over-instrument |
| LLM calls found | Add LLM observability section (see below) |
| Error tracker exists | Ensure new code integrates with it |

---

## Step 1: Define What "Working" Looks Like

Telemetry without a question is noise. Before instrumenting anything, write down 2–4 questions an on-call engineer (or you, at 2am) will ask about this feature:

```
FEATURE: [name]
QUESTIONS THAT NEED TO BE ANSWERABLE:
1. Is it succeeding or failing, and at what rate?
2. How fast is it? (not average - p95/p99)
3. When it fails, why? (what's the error, which dependency, which input?)
4. [For agents] Is it stuck, looping, or spending more than expected?

→ Every signal added must answer one of these questions.
   If a log line or metric doesn't map to a question, don't add it.
```

---

## Step 2: Structured Logging

Log events, not prose. Every log line is a machine-readable object with a stable event name and typed fields. Prose logs can't be queried, filtered, or alerted on.

```
// BAD: prose - tells you something happened, not what or why
console.log(`Payment ${id} failed after ${n} retries`);
logger.info("Processing request")

// GOOD: structured - every field is queryable
logger.warn({
  event: 'payment_failed',
  paymentId: id,
  provider: 'stripe',
  errorCode: err.code,
  attempt: n,
  durationMs: elapsed,
});
```

### Log Levels - Use Consistently

| Level | Meaning | On-call action |
|---|---|---|
| `error` | Something broke that needs attention | Investigate now |
| `warn` | Degraded but handled (retry succeeded, fallback used) | Watch for trends |
| `info` | Significant business event (job started/finished, user action) | None |
| `debug` | Diagnostic detail | Off in production by default |

Never log at `error` for things you're handling. Never log at `info` for every function call. The signal-to-noise ratio of your logs is as important as coverage.

### Correlation IDs - Mandatory

Without a correlation/request ID on every log line, you cannot reconstruct a single request from interleaved production logs. Generate at the system boundary, propagate everywhere.

**Node.js:**
```typescript
import { randomUUID } from 'crypto';

// Middleware - generate or accept incoming ID
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] ?? randomUUID();
  req.log = logger.child({ requestId: req.id, path: req.path });
  res.setHeader('x-request-id', req.id);
  next();
});

// Pass to outbound calls
await fetch(upstreamUrl, {
  headers: { 'x-request-id': req.id }
});
```

**Python:**
```python
import uuid
from contextvars import ContextVar

request_id: ContextVar[str] = ContextVar('request_id', default='')

# FastAPI middleware
@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    rid = request.headers.get('x-request-id', str(uuid.uuid4()))
    request_id.set(rid)
    response = await call_next(request)
    response.headers['x-request-id'] = rid
    return response

# In structlog processor - auto-attaches to every log call
def add_request_id(logger, method, event_dict):
    event_dict['request_id'] = request_id.get()
    return event_dict
```

**Rust:**
```rust
// Using tracing crate - propagate via span fields
let span = tracing::info_span!("handle_request",
    request_id = %request_id,
    path = %path
);
let _guard = span.enter();
// All tracing calls inside inherit these fields
```

### Stack Defaults (if no logger exists)

| Stack | Recommended | Why |
|---|---|---|
| Node.js | `pino` | Fastest, structured by default, JSON output |
| Python | `structlog` + stdlib `logging` | Structured, composable processors |
| Rust | `tracing` crate | Async-aware, integrates with OpenTelemetry |
| Go | `zap` or `slog` (stdlib) | Fast, structured |
| Any | OpenTelemetry Logs | If already using OTel for traces/metrics |

---

## Step 3: Metrics

Metrics tell you **that** something is wrong and **how often**. For every endpoint and every external dependency, instrument **RED**: **R**ate, **E**rrors, **D**uration. For resources (queues, DB pools, caches), use **USE**: **U**tilization, **S**aturation, **E**rrors.

Never track averages. Always use histograms so p50/p95/p99 are queryable. An average hides the 1% of users having a terrible time.

### Cardinality - The Most Common Failure Mode

Every unique label combination is a separate time series. High-cardinality labels (user IDs, raw URLs, error messages) will crash your metrics backend.

```
✅ OK as label:    route="/api/tasks/:id"   status="5xx"   provider="stripe"
❌ Never a label:  user_id, email, request_id, raw URL, full error message text
```

High-cardinality lookups (find me everything for user X) belong in logs and traces - not metrics.

### Node.js (prom-client)
```typescript
import { Histogram, Counter, register } from 'prom-client';

const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request latency',
  labelNames: ['method', 'route', 'status_class'],
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
});

const httpErrors = new Counter({
  name: 'http_errors_total',
  help: 'Total HTTP errors',
  labelNames: ['method', 'route', 'status_class'],
});

// Middleware
app.use((req, res, next) => {
  const end = httpDuration.startTimer();
  res.on('finish', () => {
    const statusClass = `${Math.floor(res.statusCode / 100)}xx`;
    end({ method: req.method, route: req.route?.path ?? 'unknown', status_class: statusClass });
    if (res.statusCode >= 400) {
      httpErrors.inc({ method: req.method, route: req.route?.path ?? 'unknown', status_class: statusClass });
    }
  });
  next();
});
```

### Python (prometheus-client)
```python
from prometheus_client import Histogram, Counter, start_http_server

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'route', 'status_class'],
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]
)

REQUEST_ERRORS = Counter(
    'http_errors_total',
    'Total HTTP errors',
    ['method', 'route', 'status_class']
)

# FastAPI middleware
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    status_class = f"{response.status_code // 100}xx"
    route = request.url.path  # Use route template in real impl
    REQUEST_DURATION.labels(request.method, route, status_class).observe(duration)
    if response.status_code >= 400:
        REQUEST_ERRORS.labels(request.method, route, status_class).inc()
    return response
```

### Rust (metrics crate)
```rust
use metrics::{counter, histogram};

// In handler
let start = std::time::Instant::now();
let result = handle_request(&req).await;
let duration = start.elapsed().as_secs_f64();

histogram!("http_request_duration_seconds",
    "route" => route,
    "status_class" => status_class
).record(duration);

if result.is_err() {
    counter!("http_errors_total", "route" => route).increment(1);
}
```

---

## Step 4: Distributed Tracing

Traces tell you **where** time went across service boundaries and async operations. Only add tracing if the project has cross-service calls, background jobs, queues, or complex async chains. A single-process script doesn't need it.

Use **OpenTelemetry** - vendor-neutral, works with any backend (Jaeger, Tempo, Datadog, Honeycomb). Auto-instrumentation covers HTTP, DB clients, and common frameworks with near-zero code.

### Node.js
```typescript
// tracing.ts - import BEFORE anything else
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';

const sdk = new NodeSDK({
  serviceName: process.env.SERVICE_NAME ?? 'unknown-service',
  traceExporter: new OTLPTraceExporter(),
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();

// Manual span for meaningful internal work
import { trace } from '@opentelemetry/api';
const tracer = trace.getTracer('my-service');

async function processPayment(id: string) {
  return tracer.startActiveSpan('process_payment', async (span) => {
    span.setAttributes({ 'payment.id': id, 'payment.provider': 'stripe' });
    try {
      const result = await chargeProvider(id);
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (err) {
      span.recordException(err);
      span.setStatus({ code: SpanStatusCode.ERROR });
      throw err;
    } finally {
      span.end();
    }
  });
}
```

### Python
```python
# tracing.py - import before app startup
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)
FastAPIInstrumentor.instrument_app(app)  # Auto-instruments all routes

tracer = trace.get_tracer(__name__)

# Manual span
async def process_job(job_id: str):
    with tracer.start_as_current_span("process_job") as span:
        span.set_attribute("job.id", job_id)
        try:
            result = await run_job(job_id)
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.StatusCode.ERROR)
            raise
```

---

## Step 5: LLM & Agent Observability

If the project scan found LLM calls or agent workflows, this section is mandatory. LLM systems have failure modes that standard observability doesn't capture: runaway costs, hallucinated tool calls, prompt injection, stuck loops, and schema drift between versions.

### What to Track Per LLM Call

```python
# Wrap every LLM call with structured observability
import time

async def llm_call_with_obs(
    prompt: str,
    model: str,
    tracer,
    logger,
    purpose: str,  # What is this call for? "summarize", "classify", "tool_select"
) -> str:
    start = time.time()

    with tracer.start_as_current_span(f"llm_call.{purpose}") as span:
        span.set_attribute("llm.model", model)
        span.set_attribute("llm.purpose", purpose)
        span.set_attribute("llm.prompt_tokens_estimate", len(prompt.split()))

        try:
            response = await client.complete(model=model, prompt=prompt)
            duration = time.time() - start

            # Metrics
            LLM_CALL_DURATION.labels(model=model, purpose=purpose).observe(duration)
            LLM_TOKENS_USED.labels(model=model, purpose=purpose).inc(response.usage.total_tokens)
            LLM_COST.labels(model=model, purpose=purpose).inc(estimate_cost(response.usage, model))

            # Structured log - DO NOT log full prompt/response (PII, secrets, cost)
            # Log shape and outcome, not content
            logger.info({
                "event": "llm_call_complete",
                "purpose": purpose,
                "model": model,
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "duration_ms": round(duration * 1000),
                "finish_reason": response.choices[0].finish_reason,
            })

            span.set_attribute("llm.completion_tokens", response.usage.completion_tokens)
            span.set_attribute("llm.finish_reason", response.choices[0].finish_reason)

            return response.choices[0].message.content

        except Exception as e:
            LLM_ERRORS.labels(model=model, purpose=purpose, error_type=type(e).__name__).inc()
            span.record_exception(e)
            logger.error({
                "event": "llm_call_failed",
                "purpose": purpose,
                "model": model,
                "error_type": type(e).__name__,
                "duration_ms": round((time.time() - start) * 1000),
            })
            raise
```

### Agent Loop Observability

```python
# Track every agent step - tool calls, decisions, outcomes
async def agent_run_with_obs(task: str, tools: list, max_iterations: int = 10):
    run_id = str(uuid.uuid4())
    start = time.time()
    iteration = 0
    total_tokens = 0
    total_cost = 0.0
    tool_call_counts: dict[str, int] = {}

    logger.info({
        "event": "agent_run_start",
        "run_id": run_id,
        "task_preview": task[:100],  # Never log full task - may contain PII
        "tools_available": [t.name for t in tools],
        "max_iterations": max_iterations,
    })

    with tracer.start_as_current_span("agent_run") as run_span:
        run_span.set_attribute("agent.run_id", run_id)
        run_span.set_attribute("agent.max_iterations", max_iterations)

        while not task_complete and iteration < max_iterations:
            iteration += 1

            with tracer.start_as_current_span(f"agent_step.{iteration}") as step_span:
                step_span.set_attribute("agent.iteration", iteration)

                # LLM decision call
                action = await llm_call_with_obs(
                    prompt=build_prompt(task, history),
                    model=model,
                    tracer=tracer,
                    logger=logger,
                    purpose="agent_action_select",
                )

                # Tool call tracking
                if action.tool_call:
                    tool_name = action.tool_call.name
                    tool_call_counts[tool_name] = tool_call_counts.get(tool_name, 0) + 1

                    # Detect suspicious repetition
                    if tool_call_counts[tool_name] > 3:
                        logger.warn({
                            "event": "agent_tool_repeated",
                            "run_id": run_id,
                            "tool": tool_name,
                            "count": tool_call_counts[tool_name],
                            "iteration": iteration,
                        })

                    with tracer.start_as_current_span(f"tool_call.{tool_name}") as tool_span:
                        tool_result = await execute_tool(action.tool_call)
                        tool_span.set_attribute("tool.name", tool_name)
                        tool_span.set_attribute("tool.success", tool_result.success)

                        logger.info({
                            "event": "agent_tool_call",
                            "run_id": run_id,
                            "iteration": iteration,
                            "tool": tool_name,
                            "success": tool_result.success,
                        })

        # Run complete
        duration = time.time() - start
        AGENT_RUN_DURATION.labels(outcome="complete" if task_complete else "max_iterations").observe(duration)

        logger.info({
            "event": "agent_run_complete",
            "run_id": run_id,
            "iterations": iteration,
            "task_complete": task_complete,
            "duration_ms": round(duration * 1000),
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(total_cost, 4),
            "tool_call_summary": tool_call_counts,
        })
```

### LLM Metrics to Track

```python
from prometheus_client import Histogram, Counter, Gauge

# Cost and token tracking
LLM_TOKENS_USED = Counter('llm_tokens_total', 'Total LLM tokens used',
    ['model', 'purpose', 'token_type'])  # token_type: prompt|completion

LLM_COST = Counter('llm_cost_usd_total', 'Estimated LLM cost in USD',
    ['model', 'purpose'])

LLM_CALL_DURATION = Histogram('llm_call_duration_seconds', 'LLM call latency',
    ['model', 'purpose'],
    buckets=[0.5, 1, 2, 5, 10, 30, 60])

LLM_ERRORS = Counter('llm_errors_total', 'LLM call failures',
    ['model', 'purpose', 'error_type'])

# Agent-specific
AGENT_RUN_DURATION = Histogram('agent_run_duration_seconds', 'Agent run duration',
    ['outcome'])  # outcome: complete | max_iterations | error | cost_limit

AGENT_ITERATIONS = Histogram('agent_iterations_per_run', 'Iterations per agent run',
    buckets=[1, 2, 3, 5, 8, 10, 15, 20])

AGENT_TOOL_CALLS = Counter('agent_tool_calls_total', 'Tool calls by agents',
    ['tool_name', 'success'])
```

### What NOT to Log in LLM Observability

```
❌ Never log:
   - Full prompt content (may contain system prompt, PII, or user data)
   - Full LLM response content (may contain sensitive generated data)
   - API keys or auth headers used for LLM calls
   - Other users' data that appeared in context

✅ Always log:
   - Token counts (prompt, completion, total)
   - Model name and version
   - Purpose/call type
   - Duration
   - Finish reason (stop, length, tool_calls, content_filter)
   - Error type (not error message - may contain prompt content)
   - Cost estimate
```

---

## Step 6: Alerting Options

Don't prescribe one alerting channel. Present the realistic options for the project's infrastructure and let the developer choose per-project. Check what exists first:

```bash
# Detect existing notification infrastructure
grep -r "telegram\|slack\|smtp\|sendgrid\|pagerduty\|webhook" \
  src/ app/ .env.example -i -l 2>/dev/null
```

### Options by Complexity

**Option A - Telegram Bot (simplest, free, solo-dev friendly)**
```python
# Works anywhere with internet. 5 minutes to set up.
import httpx

async def alert_telegram(message: str, level: str = "warn"):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    emoji = {"error": "🔴", "warn": "🟡", "info": "🟢"}.get(level, "⚪")
    await httpx.AsyncClient().post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": f"{emoji} {message}", "parse_mode": "HTML"}
    )
```

**Option B - Webhook (Slack, Discord, Teams)**
```python
# Generic webhook - same pattern for Slack/Discord/Teams
async def alert_webhook(message: str, level: str = "warn"):
    webhook_url = os.getenv("ALERT_WEBHOOK_URL")
    color = {"error": "#ff0000", "warn": "#ffaa00", "info": "#00aa00"}.get(level, "#888888")
    await httpx.AsyncClient().post(webhook_url, json={
        "text": message,  # Slack format
        "attachments": [{"color": color, "text": message}]
    })
```

**Option C - Email via SMTP (universally available)**
```python
import smtplib
from email.mime.text import MIMEText

def alert_email(subject: str, body: str):
    msg = MIMEText(body)
    msg['Subject'] = f"[ALERT] {subject}"
    msg['From'] = os.getenv("SMTP_FROM")
    msg['To'] = os.getenv("ALERT_EMAIL")
    with smtplib.SMTP_SSL(os.getenv("SMTP_HOST"), 465) as smtp:
        smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        smtp.send_message(msg)
```

**Option D - Grafana Alertmanager (if already running Prometheus/Grafana)**
```yaml
# alertmanager.yml - symptom-based rules only
groups:
  - name: service_health
    rules:
      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.01
        for: 5m
        labels:
          severity: page
        annotations:
          summary: "Error rate above 1% for 5 minutes"
          runbook: "https://your-runbook-url"

      - alert: HighLatency
        expr: histogram_quantile(0.99, http_request_duration_seconds_bucket) > 2
        for: 5m
        labels:
          severity: page
        annotations:
          summary: "p99 latency above 2s"
```

### Alert Design Rules (Stack-Agnostic)

Alert on **symptoms users feel**, not on internal causes:

```
PAGE-WORTHY (user is hurting now):     DASHBOARD ONLY (internal cause):
Error rate > 1% for 5 min             CPU at 85%
p99 latency > 2s                      Memory at 70%
Queue age > 10 min                    One pod restarted
LLM cost > $X in 1 hour               Disk at 60%
Agent stuck > N iterations             DB connections at 80%
```

Every alert must have:
1. A threshold justified by actual data or SLO - not a guess
2. A duration (don't page on a single spike)
3. A runbook - even three lines: what it means, first query to run, who to escalate to
4. An owner who will actually act on it

Two severity levels only - **page** (act now) and **ticket** (act this week). A third tier becomes noise that trains people to ignore everything.

---

## Step 7: Verify the Telemetry

Instrumentation is code - it can be wrong or silent. Before calling it done:

```
□ Force an error in dev/staging
  → Find it in logs by requestId within 30 seconds
  → Confirm every field is structured (not "[object Object]" or a Python dict repr)

□ Send normal traffic
  → Confirm metric series appear with expected labels
  → Confirm no cardinality explosion (check series count)
  → Read p95/p99 - not averages

□ If tracing: follow one request end-to-end in the trace UI
  → No broken spans, no missing services

□ If LLM/agents: run one complete agent task
  → Token counts appear in metrics
  → Cost estimate logged at run end
  → Each tool call appears as a child span

□ Fire each new alert once (lower threshold temporarily)
  → Confirm it reaches the right channel
  → Confirm runbook link works

□ Induce a failure with no source code open
  → Can you diagnose it from telemetry alone?
  → If no - what's missing?
```

---

## Red Flags - Stop and Fix

- Feature PR with external calls, retries, or queues and zero new telemetry
- Log lines built by string interpolation - unqueryable in production
- No correlation ID - every log line is an orphan
- Metrics labeled with user IDs, raw URLs, or error text (cardinality bomb)
- Latency tracked as average with no histogram
- LLM calls with no token/cost tracking
- Agent loops with no iteration counter or cost cap
- Full prompt or response content in logs (PII / secret leak risk)
- Alerts that fire daily and get acknowledged without action
- Alerts on causes (CPU) while user-facing error rate is unmonitored
- `console.log` or `print()` as the only logging in a production service

---

## Common Rationalizations

| What you think | What's actually true |
|---|---|
| "I'll add logging after it works" | The first incident with no telemetry is the most expensive moment to discover you're blind |
| "More logs = more observability" | Unstructured noise makes incidents slower. Three queryable events beat three hundred prose lines |
| "console.log is fine for now" | It can't be filtered, correlated, or alerted on. A structured logger costs five minutes once |
| "We can look at dashboards when something breaks" | Dashboards built without defined questions show you everything except the answer |
| "LLM calls are black boxes, can't observe them" | You can observe every token count, latency, cost, finish reason, and tool call - just not the content |
| "Alerting on everything important keeps us safe" | A noisy pager trains people to ignore it. The missed real page comes later |
| "User ID as a label makes debugging easier" | It makes your metrics backend fall over. High-cardinality lookups belong in logs |
