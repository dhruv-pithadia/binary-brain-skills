# HTTP metrics and Prometheus alerts

This Python `prometheus-client` pattern records every terminal outcome once and supplies every declared label. Integrate `record_request` with the framework lifecycle, including exceptions; use a fixed `unmatched` route label rather than a raw URL. Define collectors once per process registry, and configure multiprocess collection separately when applicable.

```python
from prometheus_client import Counter, Histogram

HTTP_REQUESTS = Counter(
    "http_requests_total", "Completed HTTP requests",
    ["service", "method", "route", "status_class"],
)
HTTP_DURATION = Histogram(
    "http_request_duration_seconds", "HTTP elapsed time",
    ["service", "method", "route", "status_class"],
    buckets=(0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)

def record_request(service, method, route, status_class, elapsed_seconds):
    labels = dict(service=service, method=method, route=route,
                  status_class=status_class)
    HTTP_REQUESTS.labels(**labels).inc()
    HTTP_DURATION.labels(**labels).observe(elapsed_seconds)
```

Normalize method, route, and status class to bounded sets; choose buckets around the actual latency SLO. Assign failures without a response a documented terminal status/outcome consistently. The rules below target returned 5xx responses only, not cancellations or all business failures.

## Rule files and queries

Prometheus loads rules via `rule_files` in `prometheus.yml`. Alertmanager handles grouping and notification routing; it does not load these expressions.

```yaml
# prometheus.yml fragment
rule_files:
  - service.rules.yml
```

```yaml
# service.rules.yml - example thresholds, calibrate to the service
groups:
  - name: service_health
    rules:
      - alert: HighServerErrorRate
        expr: |
          (
            sum by (service) (rate(http_requests_total{status_class="5xx"}[5m]))
            /
            sum by (service) (rate(http_requests_total[5m]))
          ) > 0.01
          and on (service)
          sum by (service) (rate(http_requests_total[5m])) > 1
        for: 5m
        labels:
          severity: page
        annotations:
          summary: "Sustained server error ratio above threshold"
      - alert: HighLatency
        expr: |
          histogram_quantile(
            0.99,
            sum by (service, le) (rate(http_request_duration_seconds_bucket[5m]))
          ) > 2
          and on (service)
          sum by (service) (rate(http_request_duration_seconds_count[5m])) > 1
        for: 5m
        labels:
          severity: page
        annotations:
          summary: "Sustained p99 request latency above threshold"
```

Apply `rate` before aggregating so counter resets are handled per series. Histogram quantiles require rates of cumulative buckets and retention of the `le` label. These rules intentionally aggregate routes and replicas by service; change both sides consistently if per-route alerts are needed. A service with no traffic should not page on a ratio; availability needs a separate health/blackbox signal. Add deployment-specific owner/runbook annotations and routing.

Validate syntax with `promtool check rules service.rules.yml` and behavior using `promtool test rules` fixtures covering counter reset, zero/low traffic, sustained failure, recovery, and multiple replicas.

Sources: [Python metric labels](https://prometheus.github.io/client_python/instrumenting/labels/), [Prometheus rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/), [rate and histogram_quantile](https://prometheus.io/docs/prometheus/latest/querying/functions/).
