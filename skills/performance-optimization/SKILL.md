---
name: performance-optimization
description: Measures, diagnoses, and fixes performance problems across any stack - frontend, backend, database, and LLM/agent workflows. Use when something is slow, when performance requirements exist, when a regression is suspected, or when profiling reveals bottlenecks. Always reads the project's CLAUDE.md, AGENTS.md, and context.md first to understand the stack, then profiles before changing anything. Never optimizes on a guess - measure, identify the real bottleneck, fix, verify.
---

# Performance Optimization

Measure before optimizing. Performance work without measurement is guessing, and guessing produces complexity that costs more than the speed it buys. Profile first, find the actual bottleneck, fix that one thing, measure again.

---

## Step 0: Understand the Project

Before profiling anything, read the project's own context files. They tell you what this is, what stack it uses, and where it stands - so you're not reverse-engineering it from scratch.

```bash
# Read the context files (created by project-initializer / session-summarizer skills)
cat CLAUDE.md 2>/dev/null
cat AGENTS.md 2>/dev/null
cat context.md 2>/dev/null

# Confirm the stack from manifests
ls package.json pyproject.toml Cargo.toml go.mod 2>/dev/null
cat package.json 2>/dev/null | grep -E "(react|vue|svelte|next|express|fastify|nest)"
cat pyproject.toml requirements.txt 2>/dev/null | grep -E "(fastapi|flask|django|pandas|numpy|asyncio)"
cat Cargo.toml 2>/dev/null | grep -E "(tokio|actix|axum|rayon)"

# Is there a frontend, backend, or both?
ls src/components src/pages app/ 2>/dev/null   # frontend signals
ls src/routes src/api app/api 2>/dev/null      # backend signals

# Are there LLM/agent calls?
grep -r "openai\|anthropic\|langchain\|completion\|agent" src/ app/ -l 2>/dev/null | head -3
```

From this, write down one line: **"This is a [frontend/backend/full-stack] [language] project using [framework], and the reported/suspected slowness is [X]."** Everything downstream flows from that.

---

## Step 1: Measure (Never Skip This)

The single most important rule: **establish a baseline with real numbers before touching code.** "It feels slow" is not a measurement. Use the symptom to decide what to profile.

```
What is slow?
├── Page load (frontend)
│   ├── Large bundle? ────────→ measure bundle size, check code splitting
│   ├── Slow server response? → measure TTFB in Network waterfall
│   └── Render-blocking? ─────→ check CSS/JS blocking in waterfall
├── Interaction (frontend)
│   ├── UI freezes? ──────────→ profile main thread for long tasks (>50ms)
│   └── Re-render storms? ────→ React DevTools Profiler / re-render count
├── API endpoint (backend)
│   ├── One endpoint slow? ───→ profile DB queries, check indexes
│   ├── All endpoints slow? ──→ check connection pool, CPU, memory
│   └── Intermittent? ────────→ lock contention, GC pauses, external deps
├── Data processing (backend)
│   ├── Slow loops? ──────────→ profile hot path, look for vectorization
│   └── Memory growth? ───────→ heap snapshot, check for leaks/unbounded caches
└── LLM / agent
    ├── Slow responses? ──────→ measure per-call latency, check model size
    ├── Expensive? ───────────→ measure tokens per call, check for bloat
    └── Sequential when parallel possible? → trace the tool-call chain
```

### Profiling Commands by Stack

**Frontend:**
```bash
# Synthetic - reproducible, good for CI
npx lighthouse https://your-url --view
# Chrome DevTools → Performance tab → Record (for interaction profiling)

# Real User Monitoring - actual user conditions
# In code:
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(console.log); onINP(console.log); onCLS(console.log);

# Bundle analysis
npx vite-bundle-visualizer        # Vite
npx webpack-bundle-analyzer        # Webpack
```

**Node.js backend:**
```bash
# CPU profiling - flamegraph
npx clinic flame -- node server.js
npx clinic doctor -- node server.js   # diagnoses event loop / GC issues
node --prof server.js && node --prof-process isolate-*.log

# Quick inline timing
console.time('db-query'); await db.query(...); console.timeEnd('db-query');
```

**Python backend:**
```bash
# Sampling profiler - low overhead, works on running process
py-spy top --pid <PID>              # live view
py-spy record -o profile.svg --pid <PID>   # flamegraph

# Deterministic profiler
python -m cProfile -o out.prof script.py
python -c "import pstats; pstats.Stats('out.prof').sort_stats('cumulative').print_stats(20)"

# Line-level
pip install line_profiler
kernprof -l -v script.py           # decorate hot functions with @profile

# Async-specific
pip install yappi                  # handles asyncio correctly
```

**Rust:**
```bash
cargo install flamegraph
cargo flamegraph --bin your-app    # flamegraph of release build

# Benchmarking
cargo bench                        # with criterion
cargo build --release              # ALWAYS profile release, never debug
```

**Database (any stack):**
```sql
-- Postgres - the single most useful command
EXPLAIN ANALYZE SELECT ... ;       -- shows actual plan + timing
-- Look for: Seq Scan on large tables, high cost, nested loops on big sets

-- Find slow queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;

-- Find missing indexes (tables with high seq scans)
SELECT relname, seq_scan, idx_scan FROM pg_stat_user_tables
WHERE seq_scan > idx_scan ORDER BY seq_scan DESC;
```

---

## Step 2: Identify the Real Bottleneck

Profiling output points to one dominant cost. Fix that - not the thing you assumed was slow. The common bottlenecks:

| Layer | Symptom | Usual cause |
|---|---|---|
| Frontend | Slow LCP | Large unoptimized images, render-blocking resources, slow TTFB |
| Frontend | Poor INP | Heavy JS on main thread, large synchronous DOM updates |
| Frontend | Re-render storms | Unstable references, missing memoization, context over-broadcast |
| Backend | Slow endpoint | N+1 queries, missing index, unbounded result set |
| Backend | All endpoints slow | Connection pool exhaustion, CPU saturation, GC pressure |
| Backend (Python) | Slow data processing | Python loops where vectorization applies, sync calls blocking async |
| Database | Slow query | Sequential scan on large table, missing/unused index, bad join order |
| LLM/Agent | Slow/expensive | Oversized model, token bloat, sequential calls, no caching |

---

## Step 3: Fix - Backend

### N+1 Queries (the most common backend killer)
```python
# BAD: one query per task to fetch its owner
tasks = await db.fetch("SELECT * FROM tasks")
for task in tasks:
    task.owner = await db.fetch_one("SELECT * FROM users WHERE id = $1", task.owner_id)

# GOOD: single query with join
tasks = await db.fetch("""
    SELECT t.*, u.name as owner_name
    FROM tasks t JOIN users u ON u.id = t.owner_id
""")
```
```typescript
// BAD - Prisma N+1
const tasks = await db.task.findMany();
for (const t of tasks) t.owner = await db.user.findUnique({ where: { id: t.ownerId } });

// GOOD - eager load
const tasks = await db.task.findMany({ include: { owner: true } });
```

### Unbounded Result Sets
```python
# BAD: load entire table into memory
all_rows = await db.fetch("SELECT * FROM orders")

# GOOD: paginate
rows = await db.fetch(
    "SELECT * FROM orders ORDER BY created_at DESC LIMIT $1 OFFSET $2",
    page_size, (page - 1) * page_size
)
# Better for large offsets: keyset pagination
rows = await db.fetch(
    "SELECT * FROM orders WHERE created_at < $1 ORDER BY created_at DESC LIMIT $2",
    last_seen_timestamp, page_size
)
```

### Missing Indexes
```sql
-- If EXPLAIN ANALYZE shows "Seq Scan" on a large table filtered by a column:
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);
-- Composite index for multi-column filters (order matters - most selective first)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
-- CONCURRENTLY avoids locking the table in production
```

### Connection Pooling
```python
# BAD: new connection per request - exhausts DB under load
async def handler():
    conn = await asyncpg.connect(DSN)  # expensive, unbounded
    ...

# GOOD: shared pool with bounds
pool = await asyncpg.create_pool(DSN, min_size=5, max_size=20)
async def handler():
    async with pool.acquire() as conn:
        ...
```

### Caching Hot Reads
```typescript
// Cache frequently-read, rarely-changed data with TTL
const cache = new Map<string, { value: unknown; expiry: number }>();
const TTL = 5 * 60 * 1000;

async function getConfig(key: string) {
  const hit = cache.get(key);
  if (hit && Date.now() < hit.expiry) return hit.value;
  const value = await db.config.findUnique({ where: { key } });
  cache.set(key, { value, expiry: Date.now() + TTL });
  return value;
}
// For multi-instance: use Redis instead of in-process Map
```

### Python-Specific: Vectorize Hot Loops
```python
# BAD: Python-level loop over a large array - slow
result = []
for price in prices:
    result.append(price * 1.05)

# GOOD: vectorized with numpy - 10-100x faster
import numpy as np
result = np.array(prices) * 1.05

# BAD: iterrows() over a DataFrame - pathologically slow
for idx, row in df.iterrows():
    df.at[idx, 'total'] = row['qty'] * row['price']

# GOOD: vectorized column operation
df['total'] = df['qty'] * df['price']
```

### Python-Specific: Don't Block the Async Loop
```python
# BAD: synchronous blocking call inside async handler - freezes the event loop
async def handler():
    data = requests.get(url)          # blocks everything
    result = heavy_cpu_computation()  # blocks everything

# GOOD: async I/O + offload CPU work to a thread/process
async def handler():
    async with httpx.AsyncClient() as client:
        data = await client.get(url)
    result = await asyncio.to_thread(heavy_cpu_computation)  # for CPU-bound
```

### Rust-Specific: Avoid Needless Clones & Blocking
```rust
// BAD: cloning a large struct just to read it
fn process(data: Vec<Record>) { ... }   // takes ownership, caller must clone
process(records.clone());

// GOOD: borrow instead
fn process(data: &[Record]) { ... }
process(&records);

// BAD: blocking call inside async - stalls the tokio worker
async fn handler() {
    let result = std::fs::read_to_string("file")?;  // blocking
}

// GOOD: async I/O or spawn_blocking for CPU work
async fn handler() {
    let result = tokio::fs::read_to_string("file").await?;
    let computed = tokio::task::spawn_blocking(|| heavy_cpu()).await?;
}

// Use rayon for data parallelism on CPU-bound work
use rayon::prelude::*;
let sums: Vec<_> = records.par_iter().map(|r| expensive(r)).collect();
```

---

## Step 4: Fix - Frontend

### Image Optimization (biggest LCP lever)
```html
<!-- BAD: no dimensions, no modern format, no priority -->
<img src="/hero.jpg" />

<!-- GOOD: LCP image - modern formats, explicit dimensions, high priority -->
<picture>
  <source srcset="/hero-800.avif 800w, /hero-1600.avif 1600w"
          sizes="(max-width: 1200px) 100vw, 1200px" type="image/avif" />
  <source srcset="/hero-800.webp 800w, /hero-1600.webp 1600w"
          sizes="(max-width: 1200px) 100vw, 1200px" type="image/webp" />
  <img src="/hero.jpg" width="1200" height="600"
       fetchpriority="high" alt="..." />
</picture>

<!-- Below-the-fold: lazy load -->
<img src="/content.webp" width="800" height="400"
     loading="lazy" decoding="async" alt="..." />
```
Explicit `width`/`height` prevent CLS. `fetchpriority="high"` on the LCP image, `loading="lazy"` on everything below the fold.

### Eliminate Unnecessary Re-renders (React)
```typescript
// BAD: new object literal every render → children always re-render
function List() {
  return <Filters options={{ sortBy: 'date', order: 'desc' }} />;
}

// GOOD: stable reference
const DEFAULT_OPTIONS = { sortBy: 'date', order: 'desc' } as const;
function List() {
  return <Filters options={DEFAULT_OPTIONS} />;
}

// Memoize expensive components and computations - but only after profiling
const Item = React.memo(function Item({ item }: Props) { /* ... */ });

function Stats({ items }: Props) {
  const stats = useMemo(() => computeStats(items), [items]); // expensive calc only
  return <div>{stats.done}/{stats.total}</div>;
}
```
Don't sprinkle `memo`/`useMemo` everywhere - overuse adds overhead and complexity. Profile, find the component that actually re-renders too much, fix that one.

### Code Splitting & Lazy Loading
```typescript
// Route-level splitting - load page code only when navigated to
const Settings = lazy(() => import('./pages/Settings'));

function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Settings />
    </Suspense>
  );
}

// Heavy, rarely-used libraries - load on demand
const loadChart = () => import('heavy-charting-lib');
```

### Modern bundlers tree-shake named imports automatically
```typescript
// This is fine in Vite / webpack 5+ if the dep ships ESM + sideEffects:false
import { debounce } from 'lodash-es';
// Don't waste time rewriting import styles - the real wins are splitting + lazy loading.
// Profile the bundle first to find what's actually large.
```

---

## Step 5: Fix - LLM & Agent Performance

If the project uses LLMs or agents, these are the highest-leverage and most-overlooked optimizations.

### Right-Size the Model
```python
# BAD: using a large, slow, expensive model for a simple task
result = await client.complete(model="large-model", prompt=classify_prompt)

# GOOD: match model to task difficulty
# Classification, extraction, routing → smallest capable model
# Complex reasoning, code generation → larger model
CLASSIFY_MODEL = "haiku-class"   # fast + cheap for simple tasks
REASONING_MODEL = "opus-class"   # only where genuinely needed
```
The biggest latency and cost win is almost always using a smaller model where it suffices. Measure quality on the actual task before assuming you need the big one.

### Cut Token Bloat
```python
# BAD: stuffing the entire context every call
prompt = f"{full_document}\n{entire_history}\n{all_examples}\nQuestion: {q}"

# GOOD: include only what this specific call needs
prompt = f"{relevant_excerpt}\nQuestion: {q}"
# - Trim history to recent/relevant turns
# - Retrieve only the relevant document chunk (don't paste the whole thing)
# - Drop few-shot examples once the model handles the task reliably
```
You pay for every input token on every call. Measure tokens per call; trimming context cuts both latency and cost.

### Parallelize Independent Calls
```python
# BAD: sequential when calls don't depend on each other
summary = await llm_call(doc1)
analysis = await llm_call(doc2)
scoring = await llm_call(doc3)
# total = sum of all three latencies

# GOOD: run independent calls concurrently
summary, analysis, scoring = await asyncio.gather(
    llm_call(doc1), llm_call(doc2), llm_call(doc3)
)
# total = latency of the slowest one
```
Same applies to independent tool calls inside an agent step.

### Cache Identical Prompts
```python
# Deterministic prompts (temperature=0) with repeated inputs → cache the result
import hashlib

def cache_key(model: str, prompt: str) -> str:
    return hashlib.sha256(f"{model}:{prompt}".encode()).hexdigest()

async def cached_llm_call(model: str, prompt: str):
    key = cache_key(model, prompt)
    if cached := await redis.get(key):
        return cached
    result = await client.complete(model=model, prompt=prompt)
    await redis.set(key, result, ex=3600)
    return result
```
Also use provider-side prompt caching (caching a long stable system prompt prefix) where available - large savings when the same context is reused across calls.

### Stream When the User Is Waiting
```python
# For user-facing responses, stream tokens as they arrive
# Perceived latency drops dramatically even if total time is the same
async for chunk in client.stream(model=model, prompt=prompt):
    yield chunk
```

---

## Step 6: Verify & Guard

A fix isn't done until you've proven it worked and prevented its return.

```
□ Before/after numbers exist - specific, not "feels faster"
  e.g. "p95 endpoint latency 850ms → 120ms"

□ The fix addressed the profiled bottleneck - not an assumed one

□ Re-profile confirms the bottleneck moved or disappeared

□ No regression in correctness - existing tests still pass

□ Guard against regression:
  - Frontend: bundle-size check + Lighthouse CI in pipeline
  - Backend: assert query count in tests (catch N+1 reintroduction)
  - LLM: track tokens/cost per run in observability (see observability skill)
```

### Performance Budgets (enforce in CI)
```
Frontend:
  JS bundle (initial):  < 200KB gzipped
  LCP:                  < 2.5s
  INP:                  < 200ms
  CLS:                  < 0.1
Backend:
  API p95:              < 200ms
  DB query p95:         < 50ms
LLM/Agent:
  Cost per run:         < $X (set per use case)
  p95 run latency:      < Ns
```
```bash
npx lhci autorun                 # Lighthouse CI for frontend
npx bundlesize                    # bundle size gate
```

---

## Red Flags

- Optimizing without a profile to justify it - the cardinal sin
- N+1 query patterns in data fetching
- List/query endpoints with no pagination or limit
- `SELECT *` on wide tables when few columns are needed
- Images without dimensions, lazy loading, or modern formats
- `React.memo`/`useMemo` sprinkled everywhere without measurement
- Python loops over large arrays/DataFrames where vectorization applies
- Synchronous/blocking calls inside async handlers
- A large LLM used for a task a small one handles
- Independent LLM/tool calls run sequentially
- Profiling a debug build (Rust) instead of release
- No before/after numbers attached to a "performance" PR

---

## Common Rationalizations

| What you think | What's actually true |
|---|---|
| "We'll optimize later" | Obvious anti-patterns (N+1, no pagination) compound fast. Fix those now; defer micro-tuning |
| "It's fast on my machine" | Your machine isn't production. Profile on representative hardware/network/data size |
| "This optimization is obvious" | If you didn't measure, you don't know. The bottleneck is often not where you think |
| "Users won't notice 100ms" | They do - research links 100ms delays to measurable drop-off |
| "The framework handles performance" | Frameworks prevent some issues but won't fix your N+1, your bundle, or your model choice |
| "Bigger model = better, just use it" | For simple tasks a small model is as good, far faster, and far cheaper. Measure the task |
