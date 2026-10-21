#!/usr/bin/env bash
# Report what this machine can do, and pick the image backend.
# Usage: detect_env.sh   (prints a summary; last line: IMAGE_BACKEND=<codex|api|host-or-diagrams>)
have() { command -v "$1" >/dev/null 2>&1; }
ok() { printf "  %-28s %s\n" "$1" "$2"; }
echo "== Study Synthesizer environment check =="
for t in python3 pdftotext pdftoppm soffice pandoc dot tesseract node; do
  if have "$t"; then ok "$t" "yes"; else ok "$t" "MISSING"; fi
done
python3 - <<'EOF'
import importlib
for m in ["pptx", "docx", "matplotlib", "PIL", "playwright", "fitz"]:
    try:
        importlib.import_module(m); print(f"  {'py:'+m:<28} yes")
    except Exception:
        print(f"  {'py:'+m:<28} MISSING")
EOF
BROWSER="${STUDY_SYNTH_BROWSER:-}"
for b in "$BROWSER" chromium chromium-browser google-chrome google-chrome-stable \
         "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
  [ -n "$b" ] && { have "$b" || [ -x "$b" ]; } && { ok "chrome/chromium" "$b"; break; }
done

IMG="host-or-diagrams"
if [ "${STUDY_SYNTH_IMAGES:-auto}" = "off" ]; then
  IMG="diagrams-only"
elif have codex; then
  if codex login status 2>&1 | grep -qi "not logged in"; then
    ok "codex" "installed, NOT logged in"
  else
    ok "codex" "installed + logged in (model: ${STUDY_SYNTH_IMAGE_MODEL:-gpt-6.1-sol})"; IMG="codex"
  fi
else
  ok "codex" "not installed"
fi
NET=$(curl -s -o /dev/null -w '%{http_code}' --max-time 6 https://api.openai.com/v1/models 2>/dev/null)
ok "api.openai.com reachable" "$([ "$NET" != "000" ] && echo "yes (HTTP $NET)" || echo "NO (blocked/offline)")"
if [ "$IMG" = "host-or-diagrams" ] && [ -n "${OPENAI_API_KEY:-}" ] && [ "$NET" != "000" ]; then IMG="api"; fi
echo "IMAGE_BACKEND=$IMG"
echo "(host-or-diagrams = use the agent's own image tool if it has one, else draw code diagrams)"
