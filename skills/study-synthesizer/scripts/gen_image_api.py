#!/usr/bin/env python3
"""Fallback image generation via the OpenAI Images API.
Usage: gen_image_api.py "<prompt>" out.png
Needs OPENAI_API_KEY and network access to api.openai.com. Model: $STUDY_SYNTH_API_IMAGE_MODEL (default gpt-image-1).
Exit codes: 0 ok | 2 no key | 4 request failed."""
import base64, json, os, sys, urllib.request

STYLE = ("Flat, clean, minimal educational illustration for a university study guide. White background, "
         "4-5 solid colours (#2E6FD8, #0F9D8A, #E07B26, #C8483B, #1F3A5F), thick outlines, large legible "
         "sans-serif labels spelled exactly as given. Not artistic, not photorealistic, no gradients, no 3D, "
         "no clutter, no logos or watermarks.")

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    prompt, out = sys.argv[1], sys.argv[2]
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("OPENAI_API_KEY not set", file=sys.stderr); sys.exit(2)
    body = {"model": os.environ.get("STUDY_SYNTH_API_IMAGE_MODEL", "gpt-image-1"),
            "prompt": f"{prompt}\n\nStyle: {STYLE}", "size": "1536x1024", "n": 1}
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.load(r)["data"][0]
    except Exception as e:  # network blocked, quota, bad model id …
        print(f"image API request failed: {e}", file=sys.stderr); sys.exit(4)
    if "b64_json" in data:
        open(out, "wb").write(base64.b64decode(data["b64_json"]))
    else:
        urllib.request.urlretrieve(data["url"], out)
    print(out)

if __name__ == "__main__":
    main()
