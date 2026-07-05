#!/usr/bin/env python3
"""MOTION QA — the wrong-speaker detector (playbook Part 6; productionized from scratch/ep3).
A single-frame audit cannot see a flapping mouth; this stacks |frame-to-frame| differences over each
dialogue plate so everything that MOVES glows red on a heatmap. The reviewer then asks per line:
does the NON-speaker's mouth glow? -> ship-blocking defect (Rule 9).

Run on explicit clips:   python -m bentley.qa.mouthmotion clip1.mp4 clip2.mp4 [--out DIR]
Run on a shotlist JSON:  python -m bentley.qa.mouthmotion --shotlist episodes/<ep>/shotlists/<l>.json
  Shotlist mode audits every plate that plays under a VO line (shots with a non-empty `vo`),
  skipping cards/titles, missing files, and `lipsync: true` pieces (synced CUs are single-speaker
  by construction). Understands both the flat animatic schema and the ep3 `seq`-based schema."""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

COLS, PER_SHEET = 3, 9


def heatmap(src, fps=8):
    """Extract low-fps frames, stack |diffs|, overlay red glow on the mid frame."""
    with tempfile.TemporaryDirectory(prefix="mouthmotion_") as td:
        tmp = Path(td)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
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
        lo = np.percentile(acc, 85)
        hi = max(np.percentile(acc, 99.7), lo + 1e-3)
        norm = np.clip((acc - lo) / (hi - lo), 0, 1)
        base = Image.open(fr[len(fr) // 2]).convert("RGB")
    red = np.zeros((*norm.shape, 3), dtype=np.uint8)
    red[..., 0] = 255
    red[..., 1] = 40
    mask = Image.fromarray((norm * 235).astype(np.uint8))
    return Image.composite(Image.fromarray(red), base, mask), float(np.percentile(acc, 99))


def plates_from_shotlist(path, root):
    """(src -> label) for every dialogue plate in a shotlist (flat or seq-based schema)."""
    data = json.loads(Path(path).read_text())
    shots = data["shots"] if isinstance(data, dict) else data
    plates = {}
    for shot in shots:
        if not shot.get("vo"):
            continue
        for p in (shot.get("seq") or [shot]):
            if p.get("lipsync"):
                continue  # synced CUs are single-speaker by construction
            src = p.get("src") or ""
            if not src or src in ("TITLE", "CARD") or not (root / src).exists():
                continue
            plates.setdefault(src, set()).add(shot.get("id", "?"))
    return {src: " ".join(sorted(ids)) for src, ids in plates.items()}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clips", nargs="*", help="video files to audit")
    ap.add_argument("--shotlist", help="shotlist JSON — audit every dialogue plate in it")
    ap.add_argument("--root", default=".", help="repo root the shotlist srcs are relative to")
    ap.add_argument("--out", default="/tmp/mouthmotion", help="output dir for the sheets")
    args = ap.parse_args(argv)

    root = Path(args.root)
    if args.shotlist:
        plates = plates_from_shotlist(args.shotlist, root)
        plates = {str(root / s): lbl for s, lbl in plates.items()}
    else:
        plates = {c: Path(c).stem for c in args.clips}
    if not plates:
        print("mouthmotion: nothing to audit (no clips / no dialogue plates found)")
        return 1

    cells = []
    for src, label in sorted(plates.items()):
        r = heatmap(src)
        if r is None:
            print(f"{Path(src).name}: too short to diff — check manually")
            continue
        img, peak = r
        cells.append((Path(src).stem, label, img))
        print(f"{Path(src).stem:24} peak={peak:5.1f}  {label}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    W, H = cells[0][2].size
    for s in range((len(cells) + PER_SHEET - 1) // PER_SHEET):
        chunk = cells[s * PER_SHEET:(s + 1) * PER_SHEET]
        rows = (len(chunk) + COLS - 1) // COLS
        sheet = Image.new("RGB", (W * COLS, (H + 34) * rows), (12, 12, 16))
        d = ImageDraw.Draw(sheet)
        for i, (name, label, img) in enumerate(chunk):
            x, y = (i % COLS) * W, (i // COLS) * (H + 34)
            sheet.paste(img, (x, y + 34))
            d.text((x + 6, y + 4), name, fill=(255, 235, 120))
            d.text((x + 6, y + 18), label[:70], fill=(160, 220, 255))
        dst = out / f"mouthmotion_sheet{s}.png"
        sheet.save(dst)
        print(f"-> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
