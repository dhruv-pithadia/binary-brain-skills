# Stack Examples

Use only the section relevant to the measured bottleneck. Adapt examples to the project's database, framework, version, and correctness requirements; they are starting points, not universal prescriptions.

## Database

### Deterministic keyset pagination

When `created_at` can repeat, use a unique tie-breaker such as the primary key in both the ordering and cursor. This example assumes non-null columns and descending order:

```sql
SELECT id, created_at, payload
FROM events
WHERE (created_at, id) < ($1, $2)
ORDER BY created_at DESC, id DESC
LIMIT $3;
```

The first page omits the cursor predicate. Match comparisons to sort direction and define null behavior explicitly. Add or adjust an index only after checking the query plan and write cost.

### Index order

Do not order composite-index columns by a simplistic "most selective first" rule. For PostgreSQL B-tree indexes, equality conditions on leading columns and then an inequality on the first non-equality column most directly constrain the scan. An index may also help satisfy ordering. Test plausible indexes against the actual query and data distribution. See the official [multicolumn index guidance](https://www.postgresql.org/docs/current/indexes-multicolumn.html) and [indexes for ordering](https://www.postgresql.org/docs/current/indexes-ordering.html).

A high sequential-scan count by itself does not diagnose a missing index. Sequential scans can be appropriate for small tables, broad reads, and favorable plans. Inspect the slow query, its plan, rows examined versus returned, table size, and workload before proposing an index.

## Python async workloads

`asyncio.to_thread()` is useful for moving blocking I/O off the event loop. Because of the GIL, it generally does not provide parallel execution for pure Python CPU-bound work. GIL-releasing extensions and free-threaded Python builds can change this behavior; verify the actual runtime. Consider a process pool or a native/vectorized operation for CPU parallelism, and measure overhead for small tasks. See [asyncio task documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread).

## React rendering

Check the installed React version, build setup, and whether React Compiler is enabled before adding `memo`, `useMemo`, or `useCallback`. When the compiler is active, it can automatically memoize components and values; manual memoization may still be useful for specific control or semantics. Profile the interaction and confirm compiler behavior in the build. See the official [React Compiler introduction](https://react.dev/learn/react-compiler/introduction) and [`memo` reference](https://react.dev/reference/react/memo).

Without a bailout, rendering a parent usually renders its child components too, even if a particular child's props appear unchanged. A memoized child may skip that render when its props are unchanged; state, context, and other updates can still render it. Sibling updates do not inherently render each other. Verify the actual cause in React DevTools Profiler rather than inferring it from the component tree.

## Profiling examples

Choose commands that match the project's existing toolchain and representative workload. Examples include:

- Browser: Chrome DevTools Performance panel; Lighthouse for repeatable page audits; bundle analyzer for transfer and parse costs.
- Node.js: built-in CPU profiles or a sampling profiler against a representative workload.
- Python: `cProfile` for call counts and cumulative time, or a sampling profiler for a running service.
- Rust: profile an optimized build and use the project's benchmark framework.
- PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS)` on a representative query, plus query statistics when available. `ANALYZE` executes the query, so account for its effects and workload before using it on production data.
