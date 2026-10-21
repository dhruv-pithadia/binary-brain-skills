#!/usr/bin/env bash
# Generate ONE non-artistic study-guide image via the Codex CLI (preferred backend).
# Usage: gen_image_codex.sh "<prompt>" <out.png> [model]
# Exit codes: 0 ok | 2 codex not installed | 3 not logged in | 4 generation failed / no image produced
set -uo pipefail
PROMPT="${1:?prompt required}"
OUT="${2:?output path required}"
MODEL="${3:-${STUDY_SYNTH_IMAGE_MODEL:-gpt-6.1-sol}}"

command -v codex >/dev/null 2>&1 || { echo "codex CLI not found" >&2; exit 2; }
LOGIN="$(codex login status 2>&1)"
if echo "$LOGIN" | grep -qi "not logged in" || ! echo "$LOGIN" | grep -qi "logged in"; then
  echo "codex is not logged in (run: codex login)" >&2; exit 3
fi

OUT_ABS="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"
WORK="$(dirname "$OUT_ABS")"
rm -f "$OUT_ABS"

STYLE="Flat, clean, minimal educational illustration for a university study guide. White or very light background, 4-5 solid colours (#2E6FD8, #0F9D8A, #E07B26, #C8483B, #1F3A5F), thick clear outlines, large legible sans-serif labels spelled exactly as given. NOT artistic, NOT photorealistic, no gradients, no 3D, no dark backgrounds, no decorative clutter, no logos or watermarks. 16:9."

codex exec \
  --skip-git-repo-check \
  --enable image_generation \
  -m "$MODEL" \
  -s workspace-write \
  -C "$WORK" \
  "Use your image generation tool to create exactly one image and save it as a PNG file at this exact path: $OUT_ABS
Image content: $PROMPT
Style requirements: $STYLE
Do not create any other files. When finished, reply only with the saved file path." \
  >"$WORK/.codex_image_log.txt" 2>&1
STATUS=$?

if [ -s "$OUT_ABS" ] && python3 - "$OUT_ABS" <<'EOF' 2>/dev/null
import sys
from PIL import Image
im = Image.open(sys.argv[1]); im.verify()
EOF
then
  echo "$OUT_ABS"; exit 0
fi
# Some Codex versions save generated images in their own output dir: find the newest image and move it (portable: no GNU find).
NEWEST="$(python3 - "$WORK" "${CODEX_HOME:-$HOME/.codex}" "$WORK/.codex_image_log.txt" <<'EOF2'
import os, sys, time
roots, ref = sys.argv[1:3], sys.argv[3]
since = os.path.getmtime(ref) - 600 if os.path.exists(ref) else time.time() - 600
best = None
for r in roots:
    for dp, dn, fn in os.walk(r):
        if dp.count(os.sep) - r.count(os.sep) > 4: continue
        for f in fn:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                p = os.path.join(dp, f); m = os.path.getmtime(p)
                if m >= since and (best is None or m > best[0]): best = (m, p)
print(best[1] if best else "")
EOF2
)"
if [ -n "$NEWEST" ] && [ "$NEWEST" != "$OUT_ABS" ]; then
  python3 -c "import sys; from PIL import Image; Image.open(sys.argv[1]).convert('RGB').save(sys.argv[2])" "$NEWEST" "$OUT_ABS" 2>/dev/null && { echo "$OUT_ABS"; exit 0; }
fi
echo "codex image generation failed (exit $STATUS); see $WORK/.codex_image_log.txt" >&2
exit 4
