# Image generation: preferred backend and fallback chain

Generated images are **optional garnish**. Precise diagrams (flows, charts, tables, stacks) are always drawn in code, because image models misspell labels. Use a generated image only when a picture of a *thing* or *scene* genuinely aids understanding (e.g. "a merchant's QR stand with a phone scanning it", "a mempool crowd waiting for a bus" metaphor).

## Backend chain (try in order, use the first that works)

### 1. Preferred: GPT image model via the Codex CLI
- Model: `$STUDY_SYNTH_IMAGE_MODEL` (default `gpt-6.1-sol`; the user can override with the exact model ID their Codex account exposes).
- Requirements: `codex` on PATH, logged in (`codex login status` shows logged in), and the `image_generation` feature (stable in recent Codex CLI releases; the script passes `--enable image_generation`).
- Run: `scripts/gen_image_codex.sh "<prompt>" <out.png> [model]`
- The script runs `codex exec` non-interactively, asks it to generate the image and save it to the path, then **verifies the file exists and is a real image**. Exit codes: 0 ok · 2 Codex missing · 3 not logged in · 4 generation failed / no file.
- **If you are the Codex agent yourself**, you can call your own image-generation tool directly with the same prompt; no need to shell out.
- **If the host supports subagents,** you may delegate the whole image batch to a subagent that runs this script, so the main agent keeps writing.

### 2. Fallback: the host agent's own image tool
If Codex is missing, not logged in, or fails, use whatever image-generation tool the current agent has natively (e.g. an image MCP server or a built-in image tool). Use the same prompt template.

### 3. Fallback: OpenAI Images API
If `OPENAI_API_KEY` is set and the network allows `api.openai.com`: `python3 scripts/gen_image_api.py "<prompt>" <out.png>` (model from `STUDY_SYNTH_API_IMAGE_MODEL`, default `gpt-image-1`).

### 4. Last resort: no image model
Replace the planned image with a code-drawn diagram (Graphviz / CSS / matplotlib) that conveys the same idea, and list in the final summary: "Image generation unavailable (<reason>); used diagrams instead."

Always check the network before blaming credentials: in sandboxed environments `api.openai.com` / `chatgpt.com` may be blocked by an allowlist. `scripts/detect_env.sh` tests this.

## Prompt template (non-artistic: mandatory)
```
Flat, clean educational diagram-style illustration for a university study guide.
Subject: <what to show, concretely>.
Show: <3–6 labelled elements, exact label text in quotes>.
Style: minimal flat vector, white or very light background, 4–5 solid colours
(#2E6FD8 blue, #0F9D8A teal, #E07B26 orange, #C8483B red, #1F3A5F navy),
thick clear outlines, large sans-serif labels, generous spacing.
Avoid: photorealism, painterly or artistic styles, gradients, 3D render,
dark moody backgrounds, decorative clutter, logos, watermarks,
any text other than the labels listed. Aspect ratio 16:9.
```
Keep the labels short (1–3 words). Fewer labels means fewer spelling errors.

## Acceptance check (inspect every image)
Reject and regenerate (max 2 retries, then fall back to a code diagram) if the image has: misspelled or invented text · wrong facts · more than ~6 labels · an artistic or photographic look · low contrast · watermark or logo. Save accepted images as `fig/img_<topic>.png` and record the prompt in `fig/image_prompts.md`.
