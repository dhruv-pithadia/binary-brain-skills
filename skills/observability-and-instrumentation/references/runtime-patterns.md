# Runtime patterns

Use the project's logger and framework middleware. Generate correlation IDs at the boundary or accept only validated IDs from trusted upstreams. Log normalized route names rather than raw paths containing user data.

## Node.js

For concurrent request context use the framework's request-scoped logger or `AsyncLocalStorage`, not a mutable global variable. A child logger should bind a generated ID and safe route metadata. Propagate IDs to dependencies along with existing trace context; do not overwrite authentication headers. On response finish or close, record one terminal event according to the framework's lifecycle, without double-counting.

## Python

Use `contextvars` for request-local context and restore its token in `finally`:

```python
from contextvars import ContextVar
from uuid import uuid4

request_id = ContextVar("request_id", default="")

@app.middleware("http")
async def correlation_middleware(request, call_next):
    rid = str(uuid4())
    token = request_id.set(rid)
    try:
        response = await call_next(request)
        response.headers["x-request-id"] = rid
        return response
    finally:
        request_id.reset(token)
```

If a trusted inbound ID is required, validate it before replacing the generated ID. Framework propagation into background tasks must be checked explicitly.

## Rust asynchronous spans

Do not hold `Span::enter()`'s guard across `.await`: another future on the same thread can inherit the wrong context. Instrument the future instead:

```rust
use tracing::Instrument;

let span = tracing::info_span!("handle_request", request_id = %request_id);
let result = handle_request(&req).instrument(span).await;
```

For `#[tracing::instrument]`, skip sensitive arguments (`skip(...)` or `skip_all`) and attach safe fields explicitly.

Sources: [Node async context](https://nodejs.org/api/async_context.html), [Python contextvars](https://docs.python.org/3/library/contextvars.html), [tracing span warnings](https://docs.rs/tracing/latest/tracing/struct.Span.html).
