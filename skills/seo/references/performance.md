# Performance and verification

Measure the part of the experience users actually wait for. Distinguish field data from a lab run, mobile from desktop, individual URLs from origin aggregates, and missing data from passing results. Field Core Web Vitals are assessed at the 75th percentile; a single local test cannot establish a field pass.

Current good thresholds are LCP at or below 2.5 seconds, INP at or below 200ms, and CLS at or below 0.1. Recheck the official guidance before using these as a reporting gate. A universal “all pages load in two seconds” rule is not an equivalent metric, and good scores do not guarantee rankings.

- **LCP:** identify the actual element, server response delay and critical resource path. Avoid lazy-loading the critical image. Use responsive sizes, caching and selective priority where justified.
- **INP:** examine interactions and main-thread work. Reduce expensive handlers, hydration and unnecessary JavaScript based on evidence. A lab total-blocking-time metric is not a measured field INP value.
- **CLS:** reserve image, video, ad and embed space. Check font loading and asynchronous UI insertion. Inspect the shift source rather than shrinking content until the score changes.

Choose image dimensions, quality and format from actual content and browser support. AVIF, WebP, JPEG, PNG and SVG each have legitimate uses. Do not convert every image blindly or destroy transparency, sharpness or accessibility. Prevent layout shifts with dimensions or aspect ratios.

When comparing a change, record build mode, URL, device/network settings, cache state, tool version and runs. Repeat noisy lab measurements and report a representative result and variation; do not call an inconclusive difference a win. Check correctness and primary user flows alongside performance.

For technical fixes, preserve repeatable evidence: response headers, status/redirect trace, emitted metadata, sitemap samples, link checks, schema validation and relevant project tests. Use an existing harness first. Keep private URLs, cookies, customer data and credentials out of artifacts intended for publication.

Search Console field/indexing reports may lag. State the observed time and coverage. With no access, distinguish confirmed HTTP/rendering facts from unverified indexing hypotheses. A recrawl request, a green build or a tool score is not proof that Google has indexed the final page.
