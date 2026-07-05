#!/usr/bin/env python3
"""Plate Match — ZERO-TOKEN background conform of a keyframe to the episode's scene-anchor plate.

Adjacent keyframes of the same scene routinely drift in sky/light color (each generation invents
its own dusk). Instead of regenerating, conform the keyframe's BACKGROUND statistics to the LOCKED
scene-anchor plate: stats are computed OUTSIDE the --protect boxes (the characters), and the
transform fades to zero INSIDE them, so Bentley/the guest keep their exact approved colors.

Usage:
  PYTHONPATH=. python -m bentley.fix.plate_match scan IMG --plate PLATE.png
      [--protect X,Y,W,H ...]
  PYTHONPATH=. python -m bentley.fix.plate_match fix IMG --plate PLATE.png
      [--protect X,Y,W,H ...] [--strength 1.0] [--feather 24] [--out OUT]

Method: Reinhard LAB statistics transfer (bentley/fix/color_transfer.py), gains clipped, blended
out over --feather px around each protect box. Always `scan` first; big deltas (L beyond ~15)
mean the keyframe's LIGHT is wrong, not just its tint — judge whether the shot still reads as the
same time-of-day before trusting a strong conform.

Honest limits: global background statistics only — it will not fix wrong CONTENT (a different
meadow, an invented object) or a cast that varies across the frame. Protect EVERY character and
canon prop; then re-run the keyframe QC side-by-side vs the master."""
import argparse
import os

import numpy as np
from PIL import Image

from bentley.fix.color_transfer import lab_stats, transfer
from bentley.fix.magic_wand import _box_blur


def _protect_mask(shape, protects):
    m = np.zeros(shape, bool)
    for (x, y, w, h) in protects or []:
        m[max(0, y):y + h, max(0, x):x + w] = True
    return m


def _blend_map(protect, feather):
    """1.0 where the transform fully applies, fading to 0.0 inside protect boxes."""
    a = 1.0 - protect.astype(np.float64)
    for _ in range(3):
        a = _box_blur(a, max(1, feather // 3))
    a[protect] = np.minimum(a[protect], 0.0)          # hard zero inside the boxes
    return np.clip(a, 0.0, 1.0)


def scan(path, plate, protects=None):
    arr = np.asarray(Image.open(path).convert("RGB"), np.float64)
    ref = np.asarray(Image.open(plate).convert("RGB"), np.float64)
    bg = ~_protect_mask(arr.shape[:2], protects)
    (tm, ts) = lab_stats(arr, bg)
    (rm, rs) = lab_stats(ref)
    d = rm - tm
    print(f"keyframe bg: L {tm[0]:6.1f}±{ts[0]:.1f}  a {tm[1]:6.1f}  b {tm[2]:6.1f}")
    print(f"plate:       L {rm[0]:6.1f}±{rs[0]:.1f}  a {rm[1]:6.1f}  b {rm[2]:6.1f}")
    print(f"delta        L {d[0]:+.1f}  a {d[1]:+.1f}  b {d[2]:+.1f}"
          + ("   << big delta — wrong LIGHT, not just tint; check time-of-day before conforming"
             if abs(d[0]) > 15 else ""))
    return d


def fix(path, plate, protects=None, strength=1.0, feather=24, out=None):
    arr = np.asarray(Image.open(path).convert("RGB"), np.float64)
    ref = np.asarray(Image.open(plate).convert("RGB"), np.float64)
    protect = _protect_mask(arr.shape[:2], protects)
    src_stats = lab_stats(arr, ~protect)
    ref_stats = lab_stats(ref)
    conformed = transfer(arr, src_stats, ref_stats, strength=1.0)
    a = (_blend_map(protect, feather) * strength)[..., None]
    out_arr = np.clip(arr * (1.0 - a) + conformed * a, 0, 255).astype(np.uint8)
    out = out or os.path.splitext(path)[0] + "_plate.png"
    Image.fromarray(out_arr).save(out)
    return out


def _roi(s):
    x, y, w, h = s.split(",")
    return int(x), int(y), int(w), int(h)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Conform a keyframe's background to the scene plate")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("scan", "fix"):
        p = sub.add_parser(name)
        p.add_argument("image")
        p.add_argument("--plate", required=True)
        p.add_argument("--protect", type=_roi, action="append")
        if name == "fix":
            p.add_argument("--strength", type=float, default=1.0)
            p.add_argument("--feather", type=int, default=24)
            p.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "scan":
        scan(a.image, a.plate, a.protect)
    else:
        print(f"conformed -> {fix(a.image, a.plate, a.protect, a.strength, a.feather, a.out)}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
