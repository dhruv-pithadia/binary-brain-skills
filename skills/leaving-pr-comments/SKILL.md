---
name: leaving-pr-comments
description: Write and verify concise, evidence-backed GitHub PR comments or review replies when posting is authorized.
---

# Leaving PR comments

Read [host execution](references/runtime.md). A review or investigation alone does not authorize posting. Use existing authorization without asking again for routine authorized replies.

Lead with the conclusion and cite code, observed behavior, or a check. Distinguish fact from judgment and explain rejected findings concretely. Read the full thread and latest code before replying. Avoid canned thanks, filler, and repeated status messages.

Follow the user's and repository's attribution conventions. Do not add a robot banner or model signature by default. Preserve text requested verbatim unless a concrete issue needs clarification. If attribution is requested, use verified public model or harness names without guessing.

Check the full comment, quotes, and attachments for secrets and unnecessary private detail. Use structured arguments or a body file to preserve Markdown and avoid shell interpolation. Inspect rendering when a permitted host tool provides it.

Verify that posting returned a comment or review URL before reporting success. Resolve a thread only after the authorized response succeeded and the finding is addressed or dismissed with evidence.
