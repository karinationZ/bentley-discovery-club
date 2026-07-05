#!/usr/bin/env python3
"""Prop Paste — ZERO-TOKEN composite of a LOCKED prop master onto a shot where it went missing.

The generators routinely eat or mangle the canon props — the Listening Tag (gold paw-print on the
teal collar), the guest's spiral shells. Instead of rerolling a whole otherwise-approved frame,
composite the prop FROM ITS LOCKED MASTER CUTOUT: position/scale/rotate, feathered edge, optional
luminance match to the destination lighting. Nothing outside the pasted footprint changes.

Usage (stills):
  PYTHONPATH=. python -m bentley.fix.prop_paste preview IMG --prop TAG_cutout.png --at X,Y
      [--scale 1.0] [--rotate 0]
  PYTHONPATH=. python -m bentley.fix.prop_paste fix IMG --prop TAG_cutout.png --at X,Y
      [--scale 1.0] [--rotate 0] [--match-light] [--feather 1.5] [--key] [--out OUT]
Usage (video — LOCKED-CAMERA shots only; the prop must sit on a static region):
  PYTHONPATH=. python -m bentley.fix.prop_paste fixvid VID --prop ... --at X,Y [...]

The prop file: an RGBA cutout made ONCE per prop from its locked master (keep next to the master,
e.g. assets/character_design/props/ListeningTag_cutout.png). A flat-background RGB master can be
keyed on the fly with --key (background = the corner color), but a curated cutout beats a key.

⚖️ OPERATOR DISCIPLINE: `preview` first (half-opacity + outline) to sit position/scale/rotation;
--match-light when the shot's lighting differs from the master's; then re-QC the region zoomed.
Honest limits: a paste is FLAT — it works where the prop faces camera on a mostly-static surface;
perspective/wrap/occlusion (collar curving around the neck, a paw over the tag) is kontext_edit
tier 3 or regen. Never paste over a moving/deforming region in video."""
import argparse
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from bentley.fix.color_transfer import lab_stats, transfer


def load_prop(path, key=False, key_tol=40.0):
    """RGBA float prop. --key: alpha from distance to the corner background color."""
    im = Image.open(path)
    if im.mode == "RGBA" and not key:
        return np.asarray(im, np.float64)
    rgb = np.asarray(im.convert("RGB"), np.float64)
    if not key:
        raise ValueError(f"{path} has no alpha channel — pass --key (flat background) or make a "
                         f"proper RGBA cutout once and keep it next to the locked master")
    corner = np.median(np.concatenate([rgb[:4, :4].reshape(-1, 3), rgb[:4, -4:].reshape(-1, 3),
                                       rgb[-4:, :4].reshape(-1, 3), rgb[-4:, -4:].reshape(-1, 3)]),
                       axis=0)
    d = np.linalg.norm(rgb - corner, axis=-1)
    alpha = np.clip((d - key_tol * 0.5) / key_tol, 0.0, 1.0) * 255.0
    return np.dstack([rgb, alpha])


def _transformed(prop_rgba, scale=1.0, rotate=0.0):
    im = Image.fromarray(np.clip(prop_rgba, 0, 255).astype(np.uint8))
    if scale != 1.0:
        im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                       Image.LANCZOS)
    if rotate:
        im = im.rotate(rotate, expand=True, resample=Image.BICUBIC)
    return np.asarray(im, np.float64)


def _composite(arr, prop, at, match_light=False, feather=1.5, opacity=1.0):
    """Alpha-composite prop (RGBA float) centered at `at` onto arr (uint8 HxWx3), in place."""
    ph, pw = prop.shape[:2]
    H, W = arr.shape[:2]
    cx, cy = at
    x0, y0 = cx - pw // 2, cy - ph // 2
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(W, x0 + pw), min(H, y0 + ph)
    if dx1 <= dx0 or dy1 <= dy0:
        raise ValueError(f"paste at {at} lands outside the {W}x{H} image")
    rgb = prop[sy0:sy0 + (dy1 - dy0), sx0:sx0 + (dx1 - dx0), :3]
    a = prop[sy0:sy0 + (dy1 - dy0), sx0:sx0 + (dx1 - dx0), 3] / 255.0
    if feather > 0:
        a = np.asarray(Image.fromarray((a * 255).astype(np.uint8))
                       .filter(ImageFilter.GaussianBlur(feather)), np.float64) / 255.0
    dest = arr[dy0:dy1, dx0:dx1].astype(np.float64)
    if match_light and (a > 0.5).sum() > 16:
        prop_stats = lab_stats(rgb, a > 0.5)
        dest_stats = lab_stats(dest)
        rgb = transfer(rgb, prop_stats, dest_stats, strength=0.75, luma_only=True)
    a3 = (a * opacity)[..., None]
    arr[dy0:dy1, dx0:dx1] = np.clip(dest * (1 - a3) + rgb * a3, 0, 255).astype(np.uint8)
    return (dx0, dy0, dx1, dy1)


def fix_image(path, prop_path, at, scale=1.0, rotate=0.0, match_light=False, feather=1.5,
              key=False, out=None):
    arr = np.asarray(Image.open(path).convert("RGB")).copy()
    prop = _transformed(load_prop(prop_path, key), scale, rotate)
    _composite(arr, prop, at, match_light, feather)
    out = out or os.path.splitext(path)[0] + "_paste.png"
    Image.fromarray(arr).save(out)
    return out


def preview_image(path, prop_path, at, scale=1.0, rotate=0.0, key=False):
    arr = np.asarray(Image.open(path).convert("RGB")).copy()
    prop = _transformed(load_prop(prop_path, key), scale, rotate)
    box = _composite(arr, prop, at, opacity=0.5)
    im = Image.fromarray(arr)
    ImageDraw.Draw(im).rectangle(box, outline=(255, 0, 80), width=2)
    out = os.path.splitext(path)[0] + "_pastepreview.png"
    im.save(out)
    return out


def fix_video(path, prop_path, at, scale=1.0, rotate=0.0, match_light=False, feather=1.5,
              key=False, out=None):
    """Same composite on every frame — LOCKED-CAMERA static-region shots ONLY."""
    prop = _transformed(load_prop(prop_path, key), scale, rotate)
    out = out or os.path.splitext(path)[0] + "_paste.mp4"
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=r_frame_rate", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip() or "24/1"
    with tempfile.TemporaryDirectory(prefix="paste_") as td:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, f"{td}/f%05d.png"],
                       check=True)
        for fn in sorted(os.listdir(td)):
            fp = os.path.join(td, fn)
            arr = np.asarray(Image.open(fp).convert("RGB")).copy()
            _composite(arr, prop, at, match_light, feather)
            Image.fromarray(arr).save(fp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", fps,
                        "-i", f"{td}/f%05d.png", "-c:v", "libx264", "-crf", "18",
                        "-pix_fmt", "yuv420p", out], check=True)
    return out


def _xy(s):
    x, y = s.split(",")
    return int(x), int(y)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Composite a locked prop cutout onto a shot")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("preview", "fix", "fixvid"):
        p = sub.add_parser(name)
        p.add_argument("target")
        p.add_argument("--prop", required=True)
        p.add_argument("--at", type=_xy, required=True)
        p.add_argument("--scale", type=float, default=1.0)
        p.add_argument("--rotate", type=float, default=0.0)
        p.add_argument("--key", action="store_true")
        if name != "preview":
            p.add_argument("--match-light", action="store_true")
            p.add_argument("--feather", type=float, default=1.5)
            p.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "preview":
        print(f"preview -> {preview_image(a.target, a.prop, a.at, a.scale, a.rotate, a.key)}")
    elif a.cmd == "fix":
        print(f"pasted -> {fix_image(a.target, a.prop, a.at, a.scale, a.rotate, a.match_light, a.feather, a.key, a.out)}")
    else:
        print(f"pasted -> {fix_video(a.target, a.prop, a.at, a.scale, a.rotate, a.match_light, a.feather, a.key, a.out)}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
