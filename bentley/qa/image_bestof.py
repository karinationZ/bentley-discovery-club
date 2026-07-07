#!/usr/bin/env python3
"""Best-of image picker — rank keyframe candidates by how ON-MODEL they are (drift lever #4).

Kling/nano-banana have NO seed, so consistency is a numbers game: generate several candidates, then
pick the one closest to the locked Bentley "DNA" reference. This turns "hand-pick 4 by eye" into a
MEASURED shortlist (the project's measured-not-eyeballed law), mirroring bentley/voices/best_of.py for
audio. The owner still approves the final — this just surfaces the best candidates and flags the
off-model ones (e.g. white paws) so a bad frame never becomes the locked keyframe a whole shot inherits.

  PYTHONPATH=. python -m bentley.qa.image_bestof --ref DNA.png cand1.png cand2.png ...
      [--coat X,Y] [--paw-region 0.35,1.0,0.2,0.8] [--sheet OUT.png] [--top 1]

Score = palette similarity to the DNA reference (pose-invariant: coat/mask/collar/blaze proportions)
MINUS a white-paw penalty (stark-white blobs in the lower body = the chronic off-canon defect). Higher
is better. Honest limits: a heuristic RANKER, not a judge — it catches palette drift and white paws,
NOT wrong ears/tail/expression. Always eyeball the top pick against the master (playbook QC) before
locking it. --coat lets you also flag coat-hue drift explicitly.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from bentley.fix.color_transfer import srgb_to_lab

# paw region as fractions of (y0,y1,x0,x1): lower-center of the frame where paws sit
PAW_REGION = (0.55, 1.0, 0.2, 0.8)
WHITE_W = 2.5          # white-paw penalty weight
COAT_W = 1.0           # coat-hue penalty weight (only when --coat given)


def _load(path, size=256):
    im = Image.open(path).convert("RGB")
    im.thumbnail((size, size))
    return np.asarray(im, np.float64)


def lab_hist(rgb, bins=6):
    """Coarse normalized LAB histogram — a pose-tolerant palette fingerprint."""
    lab = srgb_to_lab(rgb).reshape(-1, 3)
    edges = [np.linspace(0, 100, bins + 1), np.linspace(-70, 70, bins + 1), np.linspace(-70, 70, bins + 1)]
    h, _ = np.histogramdd(lab, bins=edges)
    return h.ravel() / max(h.sum(), 1)


def palette_similarity(cand_rgb, ref_hist):
    """Histogram intersection (1.0 = identical palette proportions)."""
    return float(np.minimum(lab_hist(cand_rgb), ref_hist).sum())


def white_paw_frac(rgb, region=PAW_REGION):
    """Fraction of stark-white pixels in the lower-body region (magic_wand's white-sock signature)."""
    h, w = rgb.shape[:2]
    y0, y1, x0, x1 = region
    crop = rgb[int(h * y0):int(h * y1), int(w * x0):int(w * x1)]
    if crop.size == 0:
        return 0.0
    c = crop / 255.0
    mx, mn = c.max(-1), c.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-8), 0.0)
    stark = (sat <= 0.16) & (mx >= 0.82)
    return float(stark.mean())


def coat_hue_penalty(rgb, coat_xy, ref_coat_lab):
    """LAB distance between this candidate's coat sample and the DNA coat (0 = same)."""
    x, y = coat_xy
    h, w = rgb.shape[:2]
    x = min(max(x, 4), w - 5)
    y = min(max(y, 4), h - 5)
    patch = rgb[y - 4:y + 5, x - 4:x + 5].reshape(-1, 3)
    lab = srgb_to_lab(np.median(patch, 0)[None, None, :])[0, 0]
    return float(np.linalg.norm(lab - ref_coat_lab)) / 40.0   # normalize ~1 per 40 LAB units


def rank(candidates, ref_path, coat_xy=None, region=PAW_REGION):
    ref = _load(ref_path)
    ref_hist = lab_hist(ref)
    ref_coat_lab = None
    if coat_xy:
        rh, rw = ref.shape[:2]
        # sample the DNA coat at the same relative point (assume coat_xy given in ref pixel space -> use center body)
        cx, cy = int(rw * 0.5), int(rh * 0.55)
        ref_coat_lab = srgb_to_lab(np.median(ref[cy - 4:cy + 5, cx - 4:cx + 5].reshape(-1, 3), 0)[None, None, :])[0, 0]
    rows = []
    for p in candidates:
        rgb = _load(p)
        pal = palette_similarity(rgb, ref_hist)
        wp = white_paw_frac(rgb, region)
        coat_pen = coat_hue_penalty(rgb, coat_xy, ref_coat_lab) if (coat_xy and ref_coat_lab is not None) else 0.0
        score = pal - WHITE_W * wp - COAT_W * coat_pen
        flags = []
        if wp > 0.02:
            flags.append(f"WHITE-PAWS({wp:.0%})")
        if coat_pen > 0.4:
            flags.append("COAT-DRIFT")
        rows.append({"path": str(p), "score": round(score, 4), "palette": round(pal, 3),
                     "white_paw": round(wp, 4), "coat_pen": round(coat_pen, 3), "flags": flags})
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows


def contact_sheet(rows, out, cols=4, thumb=300):
    from PIL import ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    ims = [Image.open(r["path"]).convert("RGB") for r in rows]
    for im in ims:
        im.thumbnail((thumb, thumb))
    w = max(i.width for i in ims); h = max(i.height for i in ims)
    n = len(rows); rowsn = (n + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, (h + 40) * rowsn), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for i, (r, im) in enumerate(zip(rows, ims)):
        x, y = (i % cols) * w, (i // cols) * (h + 40)
        sheet.paste(im, (x, y + 40))
        tag = f"#{i+1} {r['score']:.3f} " + (" ".join(r["flags"]) or "ok")
        d.text((x + 6, y + 10), tag[:48], fill=(255, 220, 120) if r["flags"] else (150, 230, 150), font=font)
    sheet.save(out)
    return out


def _xy(s):
    x, y = s.split(","); return int(x), int(y)


def _region(s):
    y0, y1, x0, x1 = (float(v) for v in s.split(",")); return (y0, y1, x0, x1)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rank keyframe candidates by on-model-ness vs the DNA reference")
    ap.add_argument("candidates", nargs="+")
    ap.add_argument("--ref", required=True, help="locked Bentley DNA reference (master)")
    ap.add_argument("--coat", type=_xy, help="a coat pixel in the FIRST candidate (flag coat-hue drift)")
    ap.add_argument("--paw-region", type=_region, default=PAW_REGION, help="y0,y1,x0,x1 fractions")
    ap.add_argument("--sheet", help="write a ranked contact sheet PNG")
    ap.add_argument("--top", type=int, default=1)
    a = ap.parse_args(argv)
    rows = rank(a.candidates, a.ref, a.coat, a.paw_region)
    for i, r in enumerate(rows):
        mark = "→ PICK" if i < a.top else "      "
        print(f"{mark} #{i+1}  score={r['score']:+.4f}  palette={r['palette']:.3f}  "
              f"white_paw={r['white_paw']:.3f}  {' '.join(r['flags'])}  {Path(r['path']).name}")
    if a.sheet:
        print(f"sheet -> {contact_sheet(rows, a.sheet)}")
    print(f"\nBEST: {rows[0]['path']}  (still eyeball it vs the master before locking — this ranks palette "
          f"+ white-paws, not ears/tail/expression)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
