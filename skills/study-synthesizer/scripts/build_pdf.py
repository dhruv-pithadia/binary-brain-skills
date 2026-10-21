#!/usr/bin/env python3
"""Assemble HTML parts into one document and print it to PDF.
Usage: python3 build_pdf.py <parts_dir> <out.pdf> [--css path/to/study-guide.css]
- Parts are concatenated in filename order (00_head.html, 01_..., ...). If no part contains <html>,
  a head with the skill's stylesheet is added automatically.
- Image paths in parts are resolved relative to <parts_dir>.
- Renderer: Playwright Chromium; fallback: headless Chrome/Chromium --print-to-pdf."""
import glob, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__); sys.exit(1)
    parts_dir, out = os.path.abspath(args[0]), os.path.abspath(args[1])
    css = os.path.join(HERE, "..", "assets", "study-guide.css")
    if "--css" in args:
        css = args[args.index("--css") + 1]
    parts = sorted(glob.glob(os.path.join(parts_dir, "*.html")))
    body = "".join(open(p).read() for p in parts)
    if "<html" not in body:
        body = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Study Guide</title><style>"
                + open(css).read() + "</style></head><body>" + body + "</body></html>")
    elif "</body>" not in body:
        body += "\n</body></html>"
    html_path = os.path.join(parts_dir, "_assembled.html")
    open(html_path, "w").write(body)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            kw = {}
            if os.environ.get("STUDY_SYNTH_BROWSER"):
                kw["executable_path"] = os.environ["STUDY_SYNTH_BROWSER"]
            b = p.chromium.launch(**kw); pg = b.new_page()
            pg.goto("file://" + html_path); pg.wait_for_load_state("networkidle")
            pg.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
            b.close()
    except Exception as e:
        print(f"playwright unavailable ({e}); trying headless Chrome", file=sys.stderr)
        cands = [os.environ.get("STUDY_SYNTH_BROWSER"), shutil.which("chromium"), shutil.which("chromium-browser"),
                 shutil.which("google-chrome"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
        exe = next((c for c in cands if c and os.path.exists(c)), None)
        if not exe:
            sys.exit("No Chromium/Chrome found. Install playwright (pip install playwright && playwright install chromium).")
        subprocess.run([exe, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", "file://" + html_path], check=True)
    print(out)

if __name__ == "__main__":
    main()
