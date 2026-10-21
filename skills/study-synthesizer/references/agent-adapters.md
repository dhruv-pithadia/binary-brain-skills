# Agent adapters

The skill is plain markdown plus portable scripts (bash + Python 3), so any agent with file access and a shell can run it. Notes per host:

| Host | Install location | Subagents | Image generation | Notes |
|---|---|---|---|---|
| **Claude Code** | `~/.claude/skills/study-synthesizer/` (or project `.claude/skills/`) | Task/Agent tool: use it for an independent QA review or the image batch | Shell out to `scripts/gen_image_codex.sh`; fall back per `image-generation.md` | Use the task list for phases |
| **Codex CLI / Codex in Cursor** | `~/.codex/skills/study-synthesizer/` | Spawn `codex exec` sessions for parallel units if needed | **Native**: call the image-generation tool directly with the prompt template (model `gpt-6.1-sol` or as configured) | Run with `--enable image_generation` |
| **Cursor (any model)** | Project rules / `AGENTS.md` pointing at this folder | Background agents | Codex CLI script → API fallback | Keep the work dir inside the project |
| **Gemini CLI** | `~/.gemini/` extensions or `GEMINI.md` pointing here | - | Codex CLI script if installed; else its own image tool if enabled; else code diagrams | Built-in Google Search suits Phase 3 |
| **Other agents** | Anywhere; point the agent at `SKILL.md` | - | Follow the fallback chain | - |

## Environment variables
| Variable | Default | Meaning |
|---|---|---|
| `STUDY_SYNTH_IMAGE_MODEL` | `gpt-6.1-sol` | Model passed to `codex exec -m` for image generation |
| `STUDY_SYNTH_API_IMAGE_MODEL` | `gpt-image-1` | Model for the OpenAI Images API fallback |
| `STUDY_SYNTH_IMAGES` | `auto` | `auto` = follow the chain · `off` = code diagrams only · `codex` = require Codex (fail loudly) |
| `STUDY_SYNTH_BROWSER` | auto-detect | Path to a Chromium / Chrome binary for PDF rendering |

## Delegation pattern (optional, when the host has subagents)
- **Images:** one subagent receives the list of image specs (topic, labels, out path) and runs `gen_image_codex.sh` for each, applying the acceptance check, then returns the accepted file list.
- **QA:** one fresh subagent receives the PDF path, the sources folder and `qa-checklist.md`, and returns a defect list with page numbers.
- **Research:** a subagent may run Phase 3 and write `research_brief.md`; any available model is fine.
The main agent always does the writing, integration and final check.
