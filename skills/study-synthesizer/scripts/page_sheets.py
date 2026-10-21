#!/usr/bin/env python3
"""Render a PDF into contact sheets (18 pages per sheet) for visual QA, and flag near-empty pages.
Usage: python3 page_sheets.py <file.pdf> <out_dir> [dpi=45]"""
import glob, os, subprocess, sys
from PIL import Image

def main():
    pdf, out = sys.argv[1], sys.argv[2]
    dpi = sys.argv[3] if len(sys.argv) > 3 else "45"
    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, "p-*.png")): os.remove(f)
    subprocess.run(["pdftoppm", "-r", dpi, "-png", pdf, os.path.join(out, "p")], check=True)
    files = sorted(glob.glob(os.path.join(out, "p-*.png")))
    ims = [Image.open(f).convert("RGB") for f in files]
    w, h = ims[0].size; cols = 6
    for k in range(0, len(ims), 18):
        ch = ims[k:k+18]; rows = (len(ch) + cols - 1) // cols
        g = Image.new("RGB", (w*cols, h*rows), "white")
        for i, im in enumerate(ch): g.paste(im, ((i % cols)*w, (i//cols)*h))
        g.save(os.path.join(out, f"sheet{k//18}.jpg"), quality=80)
    # near-empty page detector (ink coverage below threshold, ignoring the cover)
    flagged = []
    for i, im in enumerate(ims[1:], 2):
        hist = im.convert("L").histogram()
        ink = sum(hist[:200]) / sum(hist)
        if ink < 0.035: flagged.append((i, round(ink*100, 1)))
    print(f"{len(ims)} pages -> {out}/sheet*.jpg")
    if flagged:
        print("NEAR-EMPTY pages (check for spill-over):", ", ".join(f"p{p} ({v}% ink)" for p, v in flagged))

if __name__ == "__main__":
    main()
