---
name: demo
description: "Create a narrated vertical explainer reel with verified narration, word timing, presenter animation, sound, and MP4 delivery using the actual target machine's measured rendering budget. Not for standalone transcription or generic video edits."
---

# Demo

Build a short, understandable lesson, not a collection of animated labels. Each demonstration must illustrate the spoken claim. Default to a 30–60 second 9:16 reel with an original 2D presenter, captions and a limited palette. Follow the user's topic, required facts, destination and chosen style instead of imposing this template on every video.

## 1. Resume or brief

Read existing project files before changing anything. For a new reel, ask for the topic and required points if missing. Infer audience and purpose from the request, asking only consequential gaps. Draft a two-line hook, three to seven points as duration permits, and one closing payoff. Check factual claims and avoid invented statistics, testimonials and covert advertising.

Show the script before generating narration unless the user has already approved it or explicitly authorized autonomous script choices. Record the accepted script in `script.txt`. If voice is undecided, generate a short hook sample with up to three suitable voices using the selected provider, then ask for the choice once. Existing voice choices skip this step. Do not record a full script three times.

Load `hyperframes` before executing the video workflow and use its routing, brief and lifecycle contracts. A custom talking SVG presenter can use `general-video`; simpler topic explainers may fit the specialized route. Persist these recipe constraints in `BRIEF.md` without restarting an answered interview. If required skills or tools are unavailable, report the exact missing capability rather than pretending the workflow ran.

## 2. Check the machine and choose a feasible budget

Read [hardware constraints](references/hardware.md). Inspect the actual target machine and choose its budget from measured resources. Do not assume the reference author's hardware belongs to this user. Run the read-only helper:

```sh
python3 <skill-dir>/scripts/doctor.py --project <project-dir>
```

It reports real RAM, current free disk, required CLI availability and optional Blender detection without installing anything. Keep persistent machine facts separate from current free disk and available memory. Inspect current memory pressure before heavy work with permitted host diagnostics; total RAM is not free RAM.

Default to HTML/CSS/SVG at 30fps, one active heavy process, and a 540×960 draft. Test a representative 3–5 second segment before a full render. Attempt 1080×1920 only after that test is stable; report any lower-resolution delivery. Do not claim that a short test guarantees a whole film will fit.

Check installed command help before using version-sensitive flags for scale, frame rate, concurrency or quality. Do not invent HyperFrames flags. Use a lower-resolution composition/draft configuration if the CLI lacks a supported scale flag. Install only missing tools actually needed, in an isolated environment or project; report installations and downloads. Do not install Blender, large ASR/image/video models, or a new GPU stack by default.

## 3. Narration and timing

Read [audio and timing](references/audio.md) and load `media-use` for provider setup, TTS, captions and media operations. Choose an available local or explicitly authorized hosted provider within the budget. Reuse installed/cached assets. Record provider, voice, speed and tool versions. Never describe a metered allowance as unlimited free service or bypass a missing sign-in.

Generate the approved narration once at a natural speed; 1.1× is an optional starting point, not a fixed requirement. Edit genuine dead air only after listening. Preserve quiet consonants, breaths and meaningful pauses. Keep the original and edit map. Finalize narration before transcription/alignment; any later audio edit invalidates timestamps and envelope data.

Obtain word start/end times against the final audio, reconcile them with the exact script, and mark uncertain spans for correction. Do not distribute words evenly or invent precise timestamps. Use verified speech word starts for caption reveals, key titles, stamps and gestures. Keep long statements readable rather than animating every graphic on every word.

For a low-cost presenter envelope, convert the final narration to 16-bit PCM WAV through existing media tools, then run:

```sh
python3 <skill-dir>/scripts/analyze_audio.py <final-narration.wav> --output <project-dir>/audio-analysis.json
```

This streams PCM frames and writes duration, audio SHA-256, RMS-driven mouth poses and quiet-region candidates. It neither trims audio nor transcribes words. Loudness is an approximate talking animation, not phoneme-accurate lip sync. Retain word alignment separately.

## 4. Build the picture

Load `hyperframes-core` before authoring HTML, then the relevant animation/registry skills. Search the registry before hand-building named treatments such as halftone wipes or typing panels. Use [the visual recipe](references/design.md) as a starting direction, preserving user brand constraints.

Use an original SVG rig with separate head, eyelids/brows, glasses if desired, mouth states and hands. Draw in code; do not impersonate the source video's person. Use a seeded schedule for blinks and subtle gestures. Compute the mouth pose directly from the saved envelope at timeline time, including for backwards seeking; do not rely on a live microphone, a wall clock, or accumulating state during render.

Place one scene per point in a sub-composition with one registered paused timeline per composition. Let the framework own media playback and clip visibility. Layers are paper/background, teaching visuals, presenter, captions, then transitions. Keep the main lesson visible; the presenter must not obscure captions, statistics or device safe areas. Use local licensed fonts and meaningful word spacing.

Build from the final narration's scene boundaries. Use small content-driven pops, rises, count-ups, underlines and stamps; a diagram or demo should enact the explanation. Calm reading holds are allowed. Do not add perpetual movement merely to prevent a one-second still frame. Set initial hidden states without conflicting CSS/GSAP transforms and prevent frame-one flashes.

## 5. Sound and validation

Load the media/audio mixing skills for music, SFX and loudness. Use licensed local or authorized retrieved assets; keep an asset/rights ledger. Reuse a few coherent sounds, line them up with the visible event, and duck music below narration. Avoid a sound for every word. Measure the encoded mix; a starting integrated target near -15 LUFS and true peak at or below -1 dBTP is a delivery choice to verify, not a guaranteed result from fader values.

Run the current HyperFrames check and inspect scene beginnings, middles, captions at dense moments and transitions. Clear real failures; a lint error that prevents layout checks is not a clean audit. Follow the host's browser/device/presentation rules. In T3 use preview tools only when the request authorizes browser work, following the host's current rules. Otherwise use permitted render artifacts and inspect the images. Keep only one rendering browser active where possible.

Listen to the final audio and a representative encoded segment. Check caption accuracy and drift, monotonic word times within audio duration, mouth closure in silence, readability, presenter occlusion, looping/cut behavior and file duration. A beginning/end match is optional; do not cut speech or falsify a loop to force it.

## 6. Render and deliver

Follow the video workflow's existing approval grant and render gate; avoid redundant questions when already authorized. Render sequentially. If memory pressure, out-of-memory errors or disk constraints recur, stop the failing job, reduce one dimension of complexity and retest once. Do not launch identical retries or switch to a paid/remote renderer without authorization.

Deliver an MP4 suited to the destination, normally H.264/yuv420p with AAC for broad compatibility. Verify streams, actual dimensions, frame rate, duration and audio with `ffprobe`, then inspect the encoded artifact. Include the final path, editable project, script, alignment/envelope data, required asset credits and exact verification limits. A successful check is not proof of a successful final encode. Do not publish or upload the reel unless requested.
