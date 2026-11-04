---
name: seo
description: "Audit or improve a website's organic-search visibility, crawlability, indexing, metadata, internal linking, structured data, content quality, and search-related performance. Use for SEO audits, indexing problems, missing Google visibility, or requested SEO implementation. Not for paid ads, fabricated backlinks, guaranteed rankings, or unrelated UI redesign."
---

# SEO

Diagnose the site's actual search problem, then fix the smallest supported cause. Separate discovery, crawling, rendering, indexing, search appearance and ranking: success at one stage does not prove success at the next. Never promise a position or a deadline for indexing or rankings.

## Establish the target and intended visibility

Identify the production origin, framework, deployment mode, page templates, audience, languages and important public journeys. Use the request and repo configuration before asking questions. Distinguish a local build from the deployed site and confirm the canonical domain rather than guessing from a preview URL.

Classify route groups as public/indexable, intentionally excluded, private/authenticated, or unknown. Check staging, previews, account pages, internal search, filters, pagination and generated content before changing shared robots or metadata rules. Authentication protects private data; robots directives do not. Do not remove a restriction until the intended visibility is known.

An audit request is read-only. An implementation request authorizes relevant code changes within its scope, not automatic deployment, Search Console submission, account creation, paid tools, outreach or publishing new claims. Use available connected sources and host rules; report inaccessible evidence without inventing results.

## Gather evidence and prioritize

Inspect representative URLs from each important template, including an error page and any problematic variant. Use a bounded same-origin sample and an existing crawl or test harness when available; do not recursively crawl an unbounded site or issue high-volume external requests. Respect access limits and never bypass authentication.

Collect the facts relevant to the symptom:

- HTTP status and redirect hops, response headers and initial HTML.
- Robots rules, meta robots and `X-Robots-Tag`, including environment-specific behavior.
- Rendered main content, links, metadata and canonical when permitted tools can inspect them.
- Sitemap entries, internal-link reachability and structured-data payloads.
- Search Console indexing, selected canonical, crawl reports, queries and clicks when access exists.
- Field and lab performance with their tool, device/network conditions, timestamp and sample size.

Keep each finding tied to a URL/template or file location, observed evidence, expected behavior, user impact, proposed fix and recheck. Label hypotheses and coverage gaps. Prioritize confirmed indexing blockers and site-wide template defects before cosmetic metadata tweaks. A Lighthouse score or a `site:` search alone cannot establish indexing status.

Read [technical checks](references/technical.md), [content and search appearance](references/content.md), or [performance and verification](references/performance.md) as needed. Recheck current official guidance in [sources](references/sources.md) before depending on a feature's eligibility, a threshold, or an engine-specific policy.

## Implement selectively

Reuse the framework's existing metadata, routing, image and sitemap facilities. Prefer one correct template-level fix over hand-edited copies on every route. Preserve product behavior, data, accessibility and intentional exclusions.

Choose server rendering, static generation, prerendering or client rendering from observed content availability, crawler needs, freshness and infrastructure constraints. Do not rewrite the app merely because SSR appeared on a checklist. Do not serve deceptive content to crawlers.

Treat URL, canonical, redirect and indexing changes as connected decisions. Verify important existing URLs and their replacements before changing them. Do not introduce blanket redirects to the homepage, remove all `noindex`, generate schema for absent content, invent author identities or reviews, stuff keywords, or buy spam links.

For content requests, improve factual usefulness and search intent using the product's actual evidence. Reuse `technical-writing` when available for prose quality; do not route prose cleanup to a UI-redesign skill. Use `unslop` only if a separate visual-polish request calls for it. Neither is required for technical SEO.

## Verify and hand off

Run the project's relevant checks and examine the changed routes. Confirm emitted HTML, headers and status behavior instead of trusting configuration alone. Test both intended indexable routes and routes that must remain excluded. Where rendering matters, compare initial and rendered content using tools permitted by the host. In T3 use preview tools only when the request authorizes browser work, under the host's current rules.

Distinguish local verification, deployed verification and search-engine observations. A deployment that has not happened remains unverified in production. Search Console submission requires the user's authorization and an available verified property; prepare the exact sitemap or inspection URL otherwise. Do not report a submitted sitemap as indexed pages or an indexing request as a ranking improvement.

Report what changed or was audited, the highest-impact findings, evidence and rechecks, intentional exclusions retained, and remaining work in impact order. Include sampled scope and inaccessible sources. For ongoing measurement, define a comparable baseline and follow-up window rather than promising overnight rankings. End when the requested scope is verified or a concrete external dependency is identified.
