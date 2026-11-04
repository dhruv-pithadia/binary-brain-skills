# Technical checks

## Fetching, crawling and rendering

Check the final HTTP response rather than inferring behavior from a route file. Distinguish permanent redirects, temporary redirects, actual 404/410 responses, soft 404s and transient server errors. Shorten unnecessary redirect chains without dropping meaningful locale, auth or migration behavior. Missing pages must not all return a successful app shell or redirect to the homepage.

Compare main content and crawlable anchor links in initial HTML and, when available, the rendered page. Check blocked JS/CSS, hydration failures, lazy content, client-only metadata and navigation implemented without real link destinations. SSR or prerendering may help, but the fix should address a demonstrated limitation and preserve freshness and functionality.

Inspect robots rules for the actual host, user-agent and path, including shared defaults, deployment headers and CDN behavior. `robots.txt` controls crawling, not secure access or reliable removal from search. A crawler must be allowed to fetch a page to observe a `noindex` directive. Inspect HTTP headers as well as HTML; a removed meta tag cannot cancel a conflicting header. Do not use `noindex` as a canonicalization workaround.

## URL consistency and canonicalization

Map preferred HTTPS/host/path forms from the intended production configuration. Check redirects, canonical links, internal links, sitemap entries and language variants for agreement. Canonical targets should be relevant, accessible and intended for indexing. Do not point all paginated or distinct pages at page one. Tracking duplicates, facets, locale versions and genuinely distinct content need different decisions. A canonical is a signal; Google may choose another URL.

For multilingual sites, verify reciprocal alternate references and valid language/region choices where applicable. Do not collapse translated pages into one language merely to eliminate duplicates. Test redirect loops, query preservation and legacy URLs after URL changes.

## Sitemaps and discovery

Use an existing generator when practical. Include intended indexable canonical URLs with absolute production origins, not preview hosts, redirects, errors, private pages or excluded variants. Escape XML correctly, use accurate modification dates, and keep generated entries synchronized with actual content. Split large maps according to current protocol limits; use a sitemap index where useful. Advertise the sitemap at the actual origin and verify its response and representative entries.

A sitemap helps discovery but does not guarantee crawling, indexing or ranking. Search Console submission and property verification are separate account actions, not code fixes.

Find orphan pages by comparing the intended public route inventory with a crawl of internal links, not just checking that a sitemap lists them. Add contextual links with descriptive anchors where they help users. Breadcrumbs should reflect a real navigable hierarchy, not a made-up route chain. Do not link every page indiscriminately or expose private pages for discoverability.
