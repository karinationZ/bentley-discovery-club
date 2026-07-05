#!/usr/bin/env python3
"""MOTION QA — the wrong-speaker detector. A single-frame audit cannot see a flapping mouth;
this stacks |frame-to-frame| differences over each dialogue plate so everything that MOVES glows
red on a heatmap. Reviewer then asks per line: does the NON-speaker's mouth glow? -> defect.
Run: python3 scratch/ep3/qa_mouthmotion.py  -> /tmp/mouthmotion_sheet*.png"""
import subprocess, importlib.util
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path("/project")
spec = importlib.util.spec_from_file_location("bs", ROOT / "episodes/ep3/build_sections.py")
bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)

# every plate that plays under a character line, with the lines it carries
plate_lines = {}
for sid, voice, vos, seq in bs.SECTIONS:
    char_lines = [l for l in vos if not l.startswith("N_")]
    if not char_lines:
        continue
    for p in seq:
        if p.get("lipsync"):
            continue  # synced CUs are single-speaker by construction
        src = p["src"]
        if src in ("TITLE", "CARD"):
            continue
        plate_lines.setdefault(src, set()).update(char_lines)

def heatmap(src, fps=8):
    """Extract low-fps frames, stack |diffs|, overlay red glow on the mid frame."""
    tmp = Path("/tmp/_mm"); tmp.mkdir(exist_ok=True)
    for f in tmp.glob("*.png"): f.unlink()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(ROOT / src),
                    "-vf", f"fps={fps},scale=640:-2", str(tmp / "f_%03d.png")], check=True)
    fr = sorted(tmp.glob("f_*.png"))
    if len(fr) < 3:
        return None
    arr = [np.asarray(Image.open(f).convert("L"), dtype=np.int16) for f in fr]
    acc = np.zeros_like(arr[0], dtype=np.float64)
    for a, b in zip(arr, arr[1:]):
        acc += np.abs(b - a)
    acc /= (len(arr) - 1)
    # show only the TOP motion: floor at p85 so ambient/camera drift stays invisible
    lo, hi = np.percentile(acc, 85), max(np.percentile(acc, 99.7), np.percentile(acc, 85) + 1e-3)
    norm = np.clip((acc - lo) / (hi - lo), 0, 1)
    base = Image.open(fr[len(fr) // 2]).convert("RGB")
    red = np.zeros((*norm.shape, 3), dtype=np.uint8); red[..., 0] = 255; red[..., 1] = 40
    overlay = Image.fromarray(red)
    mask = Image.fromarray((norm * 235).astype(np.uint8))
    return Image.composite(overlay, base, mask), float(np.percentile(acc, 99))

cells = []
for src, lines in sorted(plate_lines.items()):
    r = heatmap(src)
    if r is None:
        continue
    img, peak = r
    name = src.split("/")[-2] if "/" in src else src
    speakers = " ".join(sorted(lines))
    cells.append((name, speakers, img))
    print(f"{name:16} peak={peak:5.1f}  lines: {speakers}")

W, H = cells[0][2].size
cols = 3
per_sheet = 9
for s in range((len(cells) + per_sheet - 1) // per_sheet):
    chunk = cells[s * per_sheet:(s + 1) * per_sheet]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (W * cols, (H + 34) * rows), (12, 12, 16))
    d = ImageDraw.Draw(sheet)
    for i, (name, speakers, img) in enumerate(chunk):
        x = (i % cols) * W; y = (i // cols) * (H + 34)
        sheet.paste(img, (x, y + 34))
        d.text((x + 6, y + 4), name, fill=(255, 235, 120))
        d.text((x + 6, y + 18), speakers[:70], fill=(160, 220, 255))
    sheet.save(f"/tmp/mouthmotion_sheet{s}.png")
    print(f"-> /tmp/mouthmotion_sheet{s}.png")
