# Narration, alignment and mouth poses

Use the existing media workflow rather than building a second TTS provider system. Local Kokoro is an option when its dependencies, model and voices fit the budget; using an existing voice recording is also valid. A hosted provider requires the appropriate authorization and account. Don't copy a famous person's voice or assume permission to clone the source presenter.

## Order matters

1. Approve or otherwise authorize the script and choose the voice.
2. Generate voice, listen for pronunciation and fix errors.
3. If necessary, edit genuinely silent spans while preserving speech boundaries. Preview proposed cuts; energy thresholds cannot prove that a quiet sound contains no speech. Do not cut every pause longer than 0.24 seconds by rule.
4. Freeze final audio and retain its hash, duration and edit map.
5. Run the available transcription/alignment workflow with real word timestamps. Small Whisper-family CPU models can be a fallback; select a supported compute type and language, not a guessed Apple-GPU backend. Do not install several model families to solve one short narration.
6. Reconcile the transcript to the accepted script, checking names, numbers, contractions and omissions. Use forced alignment when available and appropriate. Human review may still be needed for uncertain words.
7. Analyze the final WAV for the presenter envelope. Regenerate both alignment and envelope whenever the voice file changes.

Use the installed media tool's timestamp schema where available; normalize only the fields the composition needs: word text, start seconds and end seconds. Keep the final-audio hash alongside it. Require finite nonnegative times, end ≥ start, monotonic ordering within the audio duration and an explicit treatment of transcript mismatches. Never fill unknown timings with evenly spaced estimates and call them verified.

## Audio analysis helper

`analyze_audio.py` accepts uncompressed 16-bit PCM WAV, mono or stereo. It computes a 30fps amplitude envelope in streaming reads. Mouth strength is clamped between -42 dBFS (closed) and -16 dBFS (open), with immediate attack and 0.55 release per frame. Ten pose indices are derived from that strength. These are visual defaults; retune after observing the recording.

The saved array includes the smoothing result, so a renderer reads pose `floor(time × fps)` rather than maintaining smoothing state during a seek. Times outside the narration close the mouth. Do not claim ten amplitude poses represent ten accurate phonemes. Use a different lip-sync pipeline only when requested and affordable.

Quiet-region candidates use 30ms RMS windows below -50 dBFS and list regions longer than 0.24 seconds. They are review hints only; no samples are removed. The helper computes its hash while reading the file rather than loading the whole recording into memory.
