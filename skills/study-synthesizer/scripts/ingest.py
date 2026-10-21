#!/usr/bin/env python3
"""Inventory a materials folder, extract text, and render pages that need visual reading.
Usage: python3 ingest.py <materials_dir> <workdir>
Writes:
  <workdir>/inventory.md            one row per file: type, pages/slides, words, flags
  <workdir>/text/<name>.txt         extracted text (per page / per slide markers)
  <workdir/render/<name>-N.png      page images for scanned PDFs and image-only slides
  <workdir>/render/<name>_grid*.png 2x2 tiles of image-only slides for fast reading
Never modifies the materials folder."""
import os, re, subprocess, sys, shutil, glob

def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def words(s): return len(re.findall(r"\w+", s or ""))

def pdf_pages(p):
    r = run(["pdfinfo", p]); m = re.search(r"Pages:\s+(\d+)", r.stdout); return int(m.group(1)) if m else 0

def render_pdf(p, out_prefix, pages=None, dpi=110):
    if pages is None:
        run(["pdftoppm", "-r", str(dpi), "-png", p, out_prefix]); return
    for n in pages:
        run(["pdftoppm", "-r", str(dpi), "-f", str(n), "-l", str(n), "-png", p, f"{out_prefix}-{n}"])

def tile(images, out_base):
    try:
        from PIL import Image
    except ImportError:
        return
    for k in range(0, len(images), 4):
        ims = [Image.open(f).convert("RGB") for f in images[k:k+4]]
        w, h = ims[0].size
        g = Image.new("RGB", (w*2, h*2), "white")
        for i, im in enumerate(ims):
            g.paste(im.resize((w, h)), ((i % 2)*w, (i//2)*h))
        g.thumbnail((1900, 1900)); g.save(f"{out_base}_grid{k//4+1}.png")

def main():
    src, work = sys.argv[1], sys.argv[2]
    tdir, rdir = os.path.join(work, "text"), os.path.join(work, "render")
    os.makedirs(tdir, exist_ok=True); os.makedirs(rdir, exist_ok=True)
    rows = []
    for root, _, files in os.walk(src):
        for f in sorted(files):
            if f.startswith(".") or f.startswith("~$"): continue
            p = os.path.join(root, f); rel = os.path.relpath(p, src)
            base = re.sub(r"[^A-Za-z0-9_-]+", "_", os.path.splitext(rel)[0])[:60]
            ext = f.lower().rsplit(".", 1)[-1] if "." in f else ""
            flags, text, units = [], "", ""
            if ext == "pdf":
                n = pdf_pages(p); text = run(["pdftotext", "-layout", p, "-"]).stdout; units = f"{n} pages"
                if words(text) < 30 * max(n, 1):
                    flags.append("SCANNED → rendered, read visually"); render_pdf(p, os.path.join(rdir, base))
            elif ext in ("pptx",):
                try:
                    from pptx import Presentation
                    prs = Presentation(p); parts, thin = [], []
                    for i, s in enumerate(prs.slides, 1):
                        t = []
                        for sh in s.shapes:
                            if sh.has_text_frame:
                                t += [pp.text.strip() for pp in sh.text_frame.paragraphs if pp.text.strip()]
                            if getattr(sh, "has_table", False) and sh.has_table:
                                t += [" | ".join(c.text for c in r.cells) for r in sh.table.rows]
                        st = " // ".join(t); parts.append(f"--- slide {i}: {st}")
                        if words(st) < 8: thin.append(i)
                    text = "\n".join(parts); units = f"{len(prs.slides)} slides"
                    if thin:
                        flags.append(f"{len(thin)} image-only slides {thin} → rendered")
                        if shutil.which("soffice"):
                            run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", rdir, p], timeout=300)
                            pdfp = os.path.join(rdir, os.path.splitext(os.path.basename(p))[0] + ".pdf")
                            if os.path.exists(pdfp):
                                render_pdf(pdfp, os.path.join(rdir, base), thin, dpi=70)
                                imgs = sorted(glob.glob(os.path.join(rdir, base + "-*.png")))
                                tile(imgs, os.path.join(rdir, base))
                        else:
                            flags.append("LibreOffice missing: cannot render image-only slides")
                except ImportError:
                    flags.append("python-pptx missing")
            elif ext in ("docx", "doc", "odt", "md", "txt", "rtf", "html"):
                if ext in ("md", "txt"):
                    text = open(p, errors="ignore").read()
                elif shutil.which("pandoc"):
                    text = run(["pandoc", p, "-t", "markdown"]).stdout
                units = f"{words(text)} words"
                if "+---" in text or re.search(r"\|\s+\|", text): flags.append("contains ASCII diagrams → replace")
            elif ext in ("png", "jpg", "jpeg", "webp", "heic"):
                flags.append("image → read visually"); units = "image"
            elif ext in ("xlsx", "csv"):
                units = "spreadsheet"
            else:
                flags.append("unhandled type")
            if text:
                open(os.path.join(tdir, base + ".txt"), "w").write(text)
            rows.append((rel, ext, units, words(text), "; ".join(flags)))
    with open(os.path.join(work, "inventory.md"), "w") as fh:
        fh.write("| File | Type | Size | Words extracted | Flags |\n|---|---|---|---|---|\n")
        for r in rows: fh.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |\n")
    print(open(os.path.join(work, "inventory.md")).read())

if __name__ == "__main__":
    main()
