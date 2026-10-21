# Research: any available model or tool

No specific research model is required. Use whatever the host provides: built-in web search, a research subagent, a browser tool, or an MCP search server. If several are available, use the cheapest one that answers the question, and go deeper only for volatile or contested facts.

## What to research (priority order)
1. **Relevance and version:** is each deck or paper from the current syllabus? Does the textbook edition match? Are any slides outdated (old stats, discontinued products)?
2. **Volatile facts:** current statistics, regulations, institutions, recent events, anything phrased "latest" or "current". Verify against a current, reputable source and cite it.
3. **Gap filling:** where slides are only headings, find the standard explanation: textbook → official or regulator sources → university course notes → reputable publications. YouTube lectures are fine to understand intuition or find a good analogy, but never the sole source for a fact.
4. **Exam framing:** common exam questions and model-answer structures for the subject (also infer them from past papers if provided).

## Source quality ladder
Official (regulators, central banks, government, standards bodies) > textbook and academic > reputable press / industry reports > company blogs > forums / videos. When sources disagree, prefer the course textbook for definitions and frameworks, and the most recent official source for figures.

## Output: `research_brief.md`
```
## <Unit / topic>
- Fact: … | Source: <title>(URL) | Date: … | Status: verified / unverified / conflicts-with-slides
- Gap filled: … | Source: …
- Relevance flags: <deck X is from 2019 and uses old regulation Y>
```
Carry citations for any researched figure into the guide (a small "Source:" note under the table or figure) and into the final summary.

## Offline mode
If there's no network, write "Research skipped: offline" in the brief, rely on the materials only, avoid stating current figures that can't be checked, and tell the user.
