#!/usr/bin/env python3
"""Recolor — ZERO-TOKEN generalized color-drift fixer (magic_wand's engine, any canon color).

magic_wand owns white→coat (paws). THIS tool owns every other color-class consistency defect:
a collar drifted off TEAL, the Listening Tag off GOLD, eyes off BROWN, Marco's golden-amber,
Indi's purple — recolored locally from a sample, texture and shading preserved, nothing outside
the boxes touched by construction. Target comes from the LOCKED master (--to-ref/--to-xy) so the
fix converges on canon, not on another drift.

Usage (stills):
  PYTHONPATH=. python -m bentley.fix.recolor preview IMG --box X,Y,W,H --from X,Y [--tol 60]
  PYTHONPATH=. python -m bentley.fix.recolor fix IMG --box X,Y,W,H [--box ...] --from X,Y
      (--to-ref MASTER.png --to-xy X,Y | --to-rgb R,G,B) [--strength 1.0] [--tol 60] [--out OUT]
Usage (video, locked-camera ROIs):
  PYTHONPATH=. python -m bentley.fix.recolor fixvid VID --roi X,Y,W,H --from X,Y
      (--to-ref ... --to-xy ... | --to-rgb ...) [--out OUT]

⚖️ OPERATOR DISCIPLINE (identical to magic_wand — every wand mis-fix traced to skipping it):
  1. ALWAYS `preview` first and LOOK at the magenta overlay — never fix on eyeballed coordinates.
  2. Boxes hug the defect: any same-colored canon detail inside a box WILL recolor with it.
  3. --from samples the DRIFTED color IN-SHOT (a click on the wrong pixel selects the wrong thing;
     the tool errors if the box contains almost nothing near the sample).
  4. Re-pass the QC gate the frame failed (zoom crop vs the master) — an unverified fix is not a fix.

Honest limits: color-only. Shape/anatomy drift (a mangled tag, a warped collar) is kontext_edit
tier 3 or regen. First production use of a new defect class: eyes-on preview + master side-by-side
before trusting the output (wand_lab law)."""
import argparse
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image

from bentley.fix.magic_wand import _box_blur, _grad_mag, _smoothstep

TOL = 60.0
BARRIER_MULT = 2.2


def sample_rgb(img_arr, xy, r=6):
    """Median RGB (float) of the patch around xy — no species check here: caller supplies
    intent via preview (the fawn validation lives in magic_wand where the target is fixed)."""
    x, y = xy
    h, w = img_arr.shape[:2]
    if not (0 <= x < w and 0 <= y < h):
        raise ValueError(f"sample {x},{y} outside image {w}x{h}")
    return np.median(img_arr[max(0, y - r):min(h, y + r + 1), max(0, x - r):min(w, x + r + 1)]
                     .reshape(-1, 3).astype(np.float64), axis=0)


def _select_weight(c, src_rgb, tol=TOL):
    """Edge-aware soft selection of pixels near src_rgb inside a box crop (float H,W,3)."""
    d = np.linalg.norm(c - src_rgb, axis=-1)
    seed = (d < tol).astype(np.float64)
    barrier = d > BARRIER_MULT * tol
    gray = c.mean(-1)
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    gm = _box_blur(_grad_mag(gray) + _grad_mag(r - b) + _grad_mag(g - b), 1)
    affinity = np.exp(-(gm * gm) / (2.0 * 18.0 ** 2))
    affinity[barrier] = 0.0
    weight = seed.copy()
    for _ in range(60):
        weight = np.maximum(_box_blur(weight, 1) * affinity, seed)
        weight[barrier] = 0.0
    for _ in range(2):
        weight = _box_blur(weight, 1)
        weight[barrier] = 0.0
    if weight.max() > 1e-6:
        weight = weight / weight.max()
    return weight, seed


def _recolor_box(arr, box, src_rgb, tgt_rgb, strength=1.0, tol=TOL):
    """Recolor pixels near src_rgb toward tgt_rgb inside one box, in place. Returns px count."""
    x, y, w, h = box
    H, W = arr.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return 0
    crop = arr[y0:y1, x0:x1]
    c = crop.astype(np.float64)
    weight, seed = _select_weight(c, src_rgb, tol)
    if seed.sum() < 8:
        raise ValueError(f"box {box}: almost no pixels near the --from sample "
                         f"(rgb={src_rgb.round(0).tolist()}) — re-aim the sample or the box")
    mask = _smoothstep(weight, 0.12 / strength, min(0.6 / strength, 0.99))
    if mask.max() < 1e-6:
        return 0
    gray = c.mean(-1)
    chroma_mag = np.linalg.norm(c - gray[..., None], axis=-1)
    tgt_gray = float(np.mean(tgt_rgb))
    tgt_chroma = tgt_rgb - tgt_gray
    tgt_cmag = float(np.linalg.norm(tgt_chroma))
    unit = tgt_chroma / max(tgt_cmag, 1e-6)
    new_cmag = np.clip(0.45 * chroma_mag + 0.55 * tgt_cmag, 0.0, max(tgt_cmag * 1.35, 12.0))
    over = np.clip(np.abs(gray - tgt_gray) / 90.0, 0.0, 1.0)
    pull = np.clip((0.22 + 0.45 * over) * strength, 0.0, 0.85)
    new_gray = (1.0 - pull) * gray + pull * tgt_gray
    recolored = new_gray[..., None] + unit[None, None, :] * new_cmag[..., None]
    m3 = mask[..., None]
    crop[...] = np.clip(c * (1.0 - m3) + recolored * m3, 0, 255).astype(arr.dtype)
    return int((mask > 0.5).sum())


def _resolve_target(to_rgb=None, to_ref=None, to_xy=None):
    if to_rgb is not None:
        return np.asarray(to_rgb, np.float64)
    if to_ref and to_xy:
        ref = np.asarray(Image.open(to_ref).convert("RGB"))
        return sample_rgb(ref, to_xy)
    raise ValueError("provide --to-rgb R,G,B or --to-ref MASTER --to-xy X,Y (sample the LOCKED master)")


def fix_image(path, boxes, from_xy=None, from_rgb=None, to_rgb=None, to_ref=None, to_xy=None,
              strength=1.0, tol=TOL, out=None):
    arr = np.asarray(Image.open(path).convert("RGB")).copy()
    src = np.asarray(from_rgb, np.float64) if from_rgb is not None else sample_rgb(arr, from_xy)
    tgt = _resolve_target(to_rgb, to_ref, to_xy)
    n = 0
    for b in boxes:
        n += _recolor_box(arr, b, src, tgt, strength, tol)
    out = out or os.path.splitext(path)[0] + "_recolor.png"
    Image.fromarray(arr).save(out)
    return out, n


def preview_image(path, boxes, from_xy=None, from_rgb=None, tol=TOL):
    arr = np.asarray(Image.open(path).convert("RGB"))
    src = np.asarray(from_rgb, np.float64) if from_rgb is not None else sample_rgb(arr, from_xy)
    mask = np.zeros(arr.shape[:2], bool)
    for (x, y, w, h) in boxes:
        c = arr[y:y + h, x:x + w].astype(np.float64)
        weight, _ = _select_weight(c, src, tol)
        mask[y:y + h, x:x + w] |= _smoothstep(weight, 0.12, 0.6) > 0.3
    if not mask.any():
        raise ValueError("empty selection — re-aim --from / widen --tol / check the box")
    ov = arr.copy()
    ov[mask] = (0.35 * ov[mask] + 0.65 * np.array([255, 0, 200])).astype(np.uint8)
    out = os.path.splitext(path)[0] + "_recolormask.png"
    Image.fromarray(ov).save(out)
    return out, int(mask.sum())


def fix_video(path, rois, from_xy, to_rgb=None, to_ref=None, to_xy=None,
              strength=1.0, tol=TOL, out=None):
    """Per-frame recolor inside each ROI. Source color re-sampled per frame -> tracks lighting;
    the TARGET stays fixed (canon does not drift with the shot)."""
    tgt = _resolve_target(to_rgb, to_ref, to_xy)
    out = out or os.path.splitext(path)[0] + "_recolor.mp4"
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=r_frame_rate", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip() or "24/1"
    with tempfile.TemporaryDirectory(prefix="recolor_") as td:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, f"{td}/f%05d.png"],
                       check=True)
        for fn in sorted(os.listdir(td)):
            fp = os.path.join(td, fn)
            arr = np.asarray(Image.open(fp).convert("RGB")).copy()
            src = sample_rgb(arr, from_xy)
            for b in rois:
                _recolor_box(arr, b, src, tgt, strength, tol)
            Image.fromarray(arr).save(fp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", fps,
                        "-i", f"{td}/f%05d.png", "-c:v", "libx264", "-crf", "18",
                        "-pix_fmt", "yuv420p", out], check=True)
    return out


def _xy(s):
    x, y = s.split(",")
    return int(x), int(y)


def _roi(s):
    x, y, w, h = s.split(",")
    return int(x), int(y), int(w), int(h)


def _rgb(s):
    r, g, b = s.split(",")
    return float(r), float(g), float(b)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Recolor — zero-token canon-color drift fixer")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preview")
    p.add_argument("image")
    p.add_argument("--box", type=_roi, action="append", required=True)
    p.add_argument("--from", dest="from_xy", type=_xy)
    p.add_argument("--from-rgb", type=_rgb)
    p.add_argument("--tol", type=float, default=TOL)
    f = sub.add_parser("fix")
    f.add_argument("image")
    f.add_argument("--box", type=_roi, action="append", required=True)
    f.add_argument("--from", dest="from_xy", type=_xy)
    f.add_argument("--from-rgb", type=_rgb)
    f.add_argument("--to-rgb", type=_rgb)
    f.add_argument("--to-ref")
    f.add_argument("--to-xy", type=_xy)
    f.add_argument("--strength", type=float, default=1.0)
    f.add_argument("--tol", type=float, default=TOL)
    f.add_argument("--out")
    v = sub.add_parser("fixvid")
    v.add_argument("video")
    v.add_argument("--roi", type=_roi, action="append", required=True)
    v.add_argument("--from", dest="from_xy", type=_xy, required=True)
    v.add_argument("--to-rgb", type=_rgb)
    v.add_argument("--to-ref")
    v.add_argument("--to-xy", type=_xy)
    v.add_argument("--strength", type=float, default=1.0)
    v.add_argument("--tol", type=float, default=TOL)
    v.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "preview":
        out, n = preview_image(a.image, a.box, a.from_xy, a.from_rgb, a.tol)
        print(f"mask {n}px -> {out}")
    elif a.cmd == "fix":
        out, n = fix_image(a.image, a.box, a.from_xy, a.from_rgb, a.to_rgb, a.to_ref, a.to_xy,
                           a.strength, a.tol, a.out)
        print(f"recolored {n}px -> {out}")
    else:
        print(f"recolored -> {fix_video(a.video, a.roi, a.from_xy, a.to_rgb, a.to_ref, a.to_xy, a.strength, a.tol, a.out)}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
