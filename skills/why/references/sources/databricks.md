# Analytics and warehouse evidence

Use analytics when the question concerns feature usage, experiments, billing, data constraints, or the empirical origin of a threshold. Do not query a warehouse merely because one is connected.

## Discover the actual schema

Inspect the available read-only connector and its supported operations. Discover catalogs, schemas, tables, columns, types, partitions, refresh cadence, and retention before querying. Names such as events, usage, exposure, and query history are search leads, not guaranteed tables. Company-specific dbt naming, column conventions, deduplication, clustering, and refresh schedules must be verified.

Bound each query by service/product scope and a relevant time window. Prefer suitable typed/curated models only after verifying their semantics. Use raw events when required and deduplicate according to the actual identity contract. Avoid broad scans and dumping private rows. Follow a returned asynchronous query handle rather than rerunning a query.

## Useful investigations

- Compare usage or error distributions around the relevant ship date, while checking instrumentation changes.
- Inspect a threshold's historical distribution before claiming it was selected from data.
- Trace experiment exposure, actual outcomes, and recorded decisions using verified flag/variant semantics.
- Check query history or data lineage when a migration or performance change concerns the warehouse itself.
- Follow a referenced notebook only if an available authorized tool can read it; SQL access does not imply notebook access.

Correlation does not establish motivation or causation. Pair data with an explicit decision record before claiming author intent. Missing retention, schema drift, sampling, late events, refresh lag, and changed instrumentation can explain apparent trends or empty results.

Return the actual fully qualified tables, exact bounded query, time window, compact aggregates, relevant dates, interpretation strength, and limitations. Keep private records out of public reports. Stop when the evidence answers the scoped question or accessible data cannot resolve it.
