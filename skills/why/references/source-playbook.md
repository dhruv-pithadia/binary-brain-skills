# Selective source playbooks

Use the playbook for a source that can answer the current question. Tool names and schemas are examples; discover the actual connector before use. Missing access is a gap. Do not search every available service by default.

| Evidence | Playbook |
| --- | --- |
| History, PR discussion, tests, ADRs | [Code archaeology](sources/code-archaeology.md) |
| Product problem and decisions | [Tickets](sources/linear.md) |
| Specs, RFCs, meeting decisions | [Documents](sources/notion.md) |
| Linked deliberation and incidents | [Chat](sources/slack.md) |
| Metrics, logs, incidents | [Infrastructure](sources/datadog.md) |
| Exception history and releases | [Errors](sources/sentry.md) |
| Feature usage, experiments, constraints | [Analytics](sources/databricks.md) |

Read [incident guidance](sources/incident-postmortem.md) when an incident lead or unexplained defensive behavior makes it relevant. A retry or null check alone does not require every source.

Independent investigators are optional. Give each a distinct assignment, question, and shared code anchor. Track cross-source leads so the parent can follow those that could change the answer.
