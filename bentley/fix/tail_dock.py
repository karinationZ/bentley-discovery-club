#!/usr/bin/env python3
"""Tail Dock — ZERO-TOKEN removal of an over-long/hairy tail on a STILL against clean background.

The docked-tail canon slips constantly (nano-banana grows her a long tail by default). When the
wrong tail sits against CLEAN background (sky, blurred meadow, water), it can be removed locally:
select the tail pixels (edge-aware, from an on-tail sample), fill the hole from the surrounding
background (multiscale diffusion + matched grain) — the stub that remains inside a --keep box is
untouched. No AI, no credits, nothing outside the boxes changes by construction.

Usage:
  PYTHONPATH=. python -m bentley.fix.tail_dock preview IMG --box X,Y,W,H --tail X,Y
      [--keep X,Y,W,H ...] [--tol 60]
  PYTHONPATH=. python -m bentley.fix.tail_dock fix IMG --box X,Y,W,H --tail X,Y
      [--keep X,Y,W,H ...] [--tol 60] [--out OUT]

⚖️ OPERATOR DISCIPLINE:
  1. `preview` FIRST — the magenta overlay must cover the WHOLE excess tail and nothing else.
  2. --box hugs the excess tail; --keep protects the canon stub / any body the box clips.
  3. --tail samples ON the drifted tail fur (the selection grows from that color).
  4. The tool WARNS on textured background (grass blades, pebbles) — a visible seam there means
     STOP: that frame is kontext_edit tier 3 ("shorten the tail to a docked stub…") or a regen.
  5. Re-QC the result zoomed against the master — an unverified fix is not a fix.

Honest limits: clean/soft backgrounds only; a tail crossing the body or another character is
NEVER this tool's job (tier 3 / regen). Stills only — video anatomy is regen-only (SKILL §1b)."""
import argparse
import os

import numpy as np
from PIL import Image

from bentley.fix.magic_wand import _box_blur
from bentley.fix.recolor import _select_weight, sample_rgb

TOL = 60.0
TEXTURE_WARN = 9.0        # high-frequency std above this = visibly textured background


def _hf_std(c, where=None):
    """Std of the high-frequency residual — the 'texture' of a region (float H,W,3 -> scalar)."""
    gray = c.mean(-1)
    hf = gray - _box_blur(gray, 2)
    return float(hf[where].std()) if where is not None and where.any() else float(hf.std())


def _diffuse_fill(c, mask, iters=(150, 80)):
    """Fill mask px from surrounding pixels: coarse pass at 1/4 scale, then full-res refine."""
    h, w = mask.shape
    small = np.asarray(Image.fromarray(np.clip(c, 0, 255).astype(np.uint8))
                       .resize((max(2, w // 4), max(2, h // 4)), Image.BILINEAR), np.float64)
    msmall = np.asarray(Image.fromarray((mask * 255).astype(np.uint8))
                        .resize((small.shape[1], small.shape[0]), Image.BILINEAR)) > 96
    for arr, m, n in ((small, msmall, iters[0]),):
        init = np.median(arr[~m].reshape(-1, 3), axis=0) if (~m).any() else np.zeros(3)
        arr[m] = init
        for _ in range(n):
            for ch in range(3):
                sm = _box_blur(arr[..., ch], 1)
                arr[..., ch][m] = sm[m]
    up = np.asarray(Image.fromarray(np.clip(small, 0, 255).astype(np.uint8))
                    .resize((w, h), Image.BILINEAR), np.float64)
    out = c.copy()
    out[mask] = up[mask]
    for _ in range(iters[1]):
        for ch in range(3):
            sm = _box_blur(out[..., ch], 1)
            out[..., ch][mask] = sm[mask]
    return out


def _tail_mask(c, tail_rgb, keeps, box_origin, tol=TOL):
    weight, seed = _select_weight(c, tail_rgb, tol)
    if seed.sum() < 8:
        raise ValueError("almost no pixels near the --tail sample inside the box — re-aim it")
    mask = weight > 0.3
    x0, y0 = box_origin
    for (kx, ky, kw, kh) in keeps or []:
        mask[max(0, ky - y0):max(0, ky - y0 + kh), max(0, kx - x0):max(0, kx - x0 + kw)] = False
    return mask


def fix_image(path, box, tail_xy, keeps=None, tol=TOL, out=None):
    arr = np.asarray(Image.open(path).convert("RGB")).copy()
    x, y, w, h = box
    H, W = arr.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    crop = arr[y0:y1, x0:x1].astype(np.float64)
    tail_rgb = sample_rgb(arr, tail_xy)
    mask = _tail_mask(crop, tail_rgb, keeps, (x0, y0), tol)
    bg_tex = _hf_std(crop, ~mask)
    filled = _diffuse_fill(crop, mask)
    # matched grain so the fill doesn't read as an airbrushed hole
    rng = np.random.default_rng(11)
    filled += (rng.normal(0.0, max(bg_tex, 0.5) * 0.7, filled.shape[:2])[..., None]) * mask[..., None]
    # feathered blend back
    a = _box_blur(mask.astype(np.float64), 2)[..., None]
    arr[y0:y1, x0:x1] = np.clip(crop * (1 - a) + filled * a, 0, 255).astype(np.uint8)
    out = out or os.path.splitext(path)[0] + "_dock.png"
    Image.fromarray(arr).save(out)
    if bg_tex > TEXTURE_WARN:
        print(f"WARN: background texture (hf-std {bg_tex:.1f} > {TEXTURE_WARN}) — inspect the fill "
              f"closely; a visible seam means kontext_edit tier 3, not this tool")
    return out, int(mask.sum())


def preview_image(path, box, tail_xy, keeps=None, tol=TOL):
    arr = np.asarray(Image.open(path).convert("RGB"))
    x, y, w, h = box
    H, W = arr.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    crop = arr[y0:y1, x0:x1].astype(np.float64)
    mask = _tail_mask(crop, sample_rgb(arr, tail_xy), keeps, (x0, y0), tol)
    ov = arr.copy()
    sub = ov[y0:y1, x0:x1]
    sub[mask] = (0.35 * sub[mask] + 0.65 * np.array([255, 0, 200])).astype(np.uint8)
    out = os.path.splitext(path)[0] + "_dockmask.png"
    Image.fromarray(ov).save(out)
    return out, int(mask.sum())


def _xy(s):
    x, y = s.split(",")
    return int(x), int(y)


def _roi(s):
    x, y, w, h = s.split(",")
    return int(x), int(y), int(w), int(h)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Tail Dock — remove an over-long tail on a still "
                                             "against clean background (zero-token)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("preview", "fix"):
        p = sub.add_parser(name)
        p.add_argument("image")
        p.add_argument("--box", type=_roi, required=True)
        p.add_argument("--tail", type=_xy, required=True)
        p.add_argument("--keep", type=_roi, action="append")
        p.add_argument("--tol", type=float, default=TOL)
        if name == "fix":
            p.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "preview":
        out, n = preview_image(a.image, a.box, a.tail, a.keep, a.tol)
        print(f"mask {n}px -> {out}")
    else:
        out, n = fix_image(a.image, a.box, a.tail, a.keep, a.tol, a.out)
        print(f"docked {n}px -> {out}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
