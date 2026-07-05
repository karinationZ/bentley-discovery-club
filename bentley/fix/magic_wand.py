#!/usr/bin/env python3
"""Magic Wand — ZERO-TOKEN local fixer for recurring color-drift defects (owner-requested 2026-07-05).

The #1 use: WHITE PAWS. Instead of a ~4cr nano-banana-edit pass (which can over-correct to red or
drift other features) or a 70cr render reroll, select the white region locally and recolor it to the
coat color SAMPLED FROM THE SAME SHOT — texture and shading are preserved, so the fix automatically
matches that shot's light. Nothing outside the selection is touched, by construction.

BOX MODE (primary, best for paws) uses the "edgeaware" engine — winner of a 3-algorithm scored
bake-off on the real EP4 hard asset (scratch/ep4/wand_lab/, 2026-07-05): confident white/cream seeds
grow through an edge-aware diffusion field; blue (ocean/sky) and high-chroma (butterflies/props) px
are hard barriers; recolor keeps per-pixel luminance texture with an adaptive pull toward the coat.
Verified collateral: butterfly Δ0.41, ocean Δ0.0, correct-coat Δ1.6 (scorer: wand_lab/score.py).

Usage (stills):
  PYTHONPATH=. python -m bentley.fix.magic_wand fix IMG --box X,Y,W,H [--box ...] --coat X,Y
      [--strength 1.0] [--out OUT]        # tight boxes around the PAWS ONLY (blaze is canon!)
  PYTHONPATH=. python -m bentley.fix.magic_wand fix IMG --seed X,Y [...] --coat X,Y
      # legacy point mode: flood-fill a connected stark-white sock from a click
  PYTHONPATH=. python -m bentley.fix.magic_wand auto IMG --coat X,Y [--out OUT]
      # find stark-white blobs in the lower half and box-fix them (classic white-sock case)
  PYTHONPATH=. python -m bentley.fix.magic_wand preview IMG --seed X,Y | --box X,Y,W,H ...
      # writes a magenta mask overlay to confirm the selection before fixing

Usage (video):
  PYTHONPATH=. python -m bentley.fix.magic_wand fixvid VID --roi X,Y,W,H [--roi ...] --coat X,Y
      # per-frame edgeaware fix inside each ROI (coat re-sampled per frame -> tracks light)

⚖️ OPERATOR DISCIPLINE (every mis-fix in the 2026-07-05 build traced to skipping this):
  1. ALWAYS run `preview` first and LOOK at the overlay — never fix on eyeballed coordinates.
  2. Boxes must fully CONTAIN the white defect with margin (a clipped defect leaves a seam), and
     hug the paw (a white flower/blaze inside the box is pixel-identical to a sock and WILL recolor).
  3. Verify the --coat sample is real fawn (the tool now rejects non-fawn samples — a collar-teal
     sample once painted the paws teal).
  4. Re-pass PAW-ZOOM QC on the result (playbook §3.2) — an unverified fix is not a fix.

Honest limits: color-only fixes. Anatomy drift (long tail, wrong pose) still needs a regen. Extreme
cream-GRADIENT caps recolor only partially at strength 1 (raise --strength, or prefer a clean
candidate). `auto` output is a PROPOSAL list for preview, never an autopilot.
"""
import argparse, os, subprocess, tempfile
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

SAT_MAX, VAL_MIN, TOL, MAX_FRAC, FEATHER = 0.28, 0.42, 70.0, 0.05, 2.0


# ---------------------------------------------------------------- shared helpers
def _box_blur(a, radius=1):
    if radius < 1:
        return a
    k = 2 * radius + 1
    pad = np.pad(a, radius, mode="edge")
    cs = np.cumsum(pad, axis=1)
    cs = np.pad(cs, ((0, 0), (1, 0)), mode="constant")
    horiz = (cs[:, k:] - cs[:, :-k]) / k
    cs = np.cumsum(horiz, axis=0)
    cs = np.pad(cs, ((1, 0), (0, 0)), mode="constant")
    return (cs[k:, :] - cs[:-k, :]) / k


def _grad_mag(gray):
    gy = np.zeros_like(gray); gx = np.zeros_like(gray)
    gy[1:-1, :] = (gray[2:, :] - gray[:-2, :]) * 0.5
    gx[:, 1:-1] = (gray[:, 2:] - gray[:, :-2]) * 0.5
    return np.sqrt(gx * gx + gy * gy)


def _smoothstep(x, lo, hi):
    t = np.clip((x - lo) / max(hi - lo, 1e-6), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _rgb_to_hsv_arr(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-8), 0.0)
    return s, mx


def _luma(rgb):
    return 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]


def sample_coat(img_arr, xy, r=8):
    """Median RGB (float 0-255) of the coat patch around xy=(x,y). VALIDATES the sample is fawn —
    a mis-aimed sample (e.g. the teal collar) once recolored paws TEAL; never trust the click."""
    x, y = xy
    h, w = img_arr.shape[:2]
    coat = np.median(img_arr[max(0, y-r):min(h, y+r+1), max(0, x-r):min(w, x+r+1)]
                     .reshape(-1, 3).astype(np.float64), axis=0)
    cr, cg, cb = coat
    if not (cr > cg > cb and (cr - cb) >= 20 and cr >= 60):
        raise ValueError(f"--coat sample at {xy} doesn't look like fawn coat (rgb={coat.round(0).tolist()}) "
                         f"— aim at clean red-fawn fur (warm, R>G>B), not the collar/blaze/background")
    return coat


# ---------------------------------------------------------------- edgeaware box engine (bake-off winner)
def _edgeaware_weight(c):
    """Soft selection weight for the white/cream defect inside a box crop (float H,W,3)."""
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    gray = c.mean(-1)
    sat = c.max(-1) - c.min(-1)
    warm = r - b
    chroma_mag = np.linalg.norm(c - gray[..., None], axis=-1)
    seed = ((gray > 132.0) & (sat < 82.0) & (warm > -6.0) & (chroma_mag < 62.0)).astype(np.float64)
    barrier = (warm < -8.0) | (chroma_mag > 95.0) | (sat > 120.0)
    gm = _box_blur(_grad_mag(gray) + _grad_mag(warm) + _grad_mag(g - b), 1)
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
    return weight, barrier, gray, chroma_mag


def _edgeaware_box(arr, box, coat_rgb, strength=1.0):
    """Recolor the white defect inside one box, in place on uint8 arr."""
    x, y, w, h = box
    H, W = arr.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return 0
    crop = arr[y0:y1, x0:x1]
    c = crop.astype(np.float64)
    weight, barrier, gray, chroma_mag = _edgeaware_weight(c)
    mask = _smoothstep(weight, 0.12 / strength, min(0.6 / strength, 0.99))
    mask[barrier] = 0.0
    if mask.max() < 1e-6:
        return 0
    coat_gray = float(coat_rgb.mean())
    coat_chroma = coat_rgb - coat_gray
    coat_cmag = float(np.linalg.norm(coat_chroma)) + 1e-6
    unit_coat = coat_chroma / coat_cmag
    tgt_cmag = np.clip(0.45 * chroma_mag + 0.55 * coat_cmag, 0.0, coat_cmag * 1.35)
    new_chroma = unit_coat[None, None, :] * tgt_cmag[..., None]
    over = np.clip((gray - coat_gray) / 90.0, 0.0, 1.0)
    pull = np.clip((0.22 + 0.45 * over) * strength, 0.0, 0.85)
    tgt_gray = (1.0 - pull) * gray + pull * coat_gray
    recolored = tgt_gray[..., None] + new_chroma
    m3 = mask[..., None]
    crop[...] = np.clip(c * (1.0 - m3) + recolored * m3, 0, 255).astype(arr.dtype)
    return int((mask > 0.5).sum())


# ---------------------------------------------------------------- legacy seed (flood) mode
def _whitish(arr, sat_max=SAT_MAX, val_min=VAL_MIN):
    f = arr.astype(np.float64) / 255.0
    s, v = _rgb_to_hsv_arr(f)
    not_blue = arr[..., 2].astype(np.int64) <= arr[..., 0].astype(np.int64) + 14
    return (s <= sat_max) & (v >= val_min) & not_blue


def _qualify(arr, seed_rgb, tol=TOL, sat_max=SAT_MAX, val_min=VAL_MIN):
    dist = np.sqrt(((arr.astype(np.float64) - seed_rgb) ** 2).sum(-1))
    return _whitish(arr, sat_max, val_min) & (dist <= tol)


def wand_mask(arr, seeds, tol=TOL, sat_max=SAT_MAX, val_min=VAL_MIN, max_frac=MAX_FRAC):
    """Point mode: flood-fill from each seed over connected whitish/seed-similar pixels."""
    h, w = arr.shape[:2]
    mask = np.zeros((h, w), bool)
    cap = int(h * w * max_frac)
    for (sx, sy) in seeds:
        if not (0 <= sx < w and 0 <= sy < h):
            raise ValueError(f"seed {sx},{sy} outside image {w}x{h}")
        seed_rgb = arr[sy, sx].astype(np.float64)
        q = _qualify(arr, seed_rgb, tol, sat_max, val_min)
        if not q[sy, sx]:
            raise ValueError(f"seed {sx},{sy} is not a whitish pixel (rgb={arr[sy,sx].tolist()}) — "
                             f"aim at the white sock/toe, or use --box mode")
        grown, dq, n = np.zeros((h, w), bool), deque([(sx, sy)]), 0
        grown[sy, sx] = True
        while dq:
            x, y = dq.popleft(); n += 1
            if n > cap:
                raise ValueError(f"selection from seed {sx},{sy} exceeded {max_frac:.0%} of the image "
                                 f"— it leaked past the paw (lower --tol)")
            for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if 0 <= nx < w and 0 <= ny < h and not grown[ny, nx] and q[ny, nx]:
                    grown[ny, nx] = True; dq.append((nx, ny))
        mask |= grown
    return mask


def recolor(arr, mask, coat_rgb, feather=FEATHER, coat_pull=0.55):
    """Per-pixel colorize under a boolean mask (seed mode): coat chroma, own luma pulled to coat."""
    out = arr.astype(np.float64).copy()
    if not mask.any():
        return arr
    coat_l = max(_luma(coat_rgb[None, :])[0], 1e-3)
    lum = _luma(out)[mask]
    blend_l = (1.0 - coat_pull) * lum + coat_pull * coat_l
    out[mask] = np.clip(coat_rgb[None, :] * (blend_l / coat_l)[:, None], 0, 255)
    a = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(feather))
    a = np.asarray(a, np.float64)[..., None] / 255.0
    return np.clip(arr.astype(np.float64) * (1 - a) + out * a, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- public API
def fix_image(path, seeds=None, coat_xy=None, out=None, tol=TOL, sat_max=SAT_MAX, val_min=VAL_MIN,
              boxes=None, strength=1.0):
    arr = np.asarray(Image.open(path).convert("RGB")).copy()
    coat = sample_coat(arr, coat_xy)
    n = 0
    if boxes:
        for b in boxes:
            n += _edgeaware_box(arr, b, coat, strength)
    if seeds:
        mask = wand_mask(arr, seeds, tol, sat_max, val_min)
        arr = recolor(arr, mask, coat)
        n += int(mask.sum())
    if not (boxes or seeds):
        raise ValueError("provide --box and/or --seed")
    out = out or os.path.splitext(path)[0] + "_wand.png"
    Image.fromarray(arr).save(out)
    return out, n


def auto_boxes(arr, y0_frac=0.45, min_px=150, max_px=25000, pad=14):
    """Classic white-sock finder: connected stark-white blobs in the lower part of the frame.
    ⚠️ PROPOSALS ONLY — it cannot tell a paw from the canon WHITE CHEST BLAZE or white flowers.
    Always `preview` the boxes and drop non-paw ones before fixing (learned on s8_run_c0: auto
    boxed the blaze + lupines)."""
    h, w = arr.shape[:2]
    f = arr.astype(np.float64) / 255.0
    s, v = _rgb_to_hsv_arr(f)
    stark = (s <= 0.16) & (v >= 0.82)
    stark[:int(h * y0_frac), :] = False
    seen = np.zeros((h, w), bool)
    out = []
    ys, xs = np.nonzero(stark)
    for sy, sx in zip(ys, xs):
        if seen[sy, sx]:
            continue
        dq = deque([(sx, sy)]); seen[sy, sx] = True; pts = []
        while dq:
            x, y = dq.popleft(); pts.append((x, y))
            for nx, ny in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if 0 <= nx < w and 0 <= ny < h and not seen[ny, nx] and stark[ny, nx]:
                    seen[ny, nx] = True; dq.append((nx, ny))
        if min_px <= len(pts) <= max_px:
            px = np.array(pts)
            x0, y0 = px[:, 0].min() - pad, px[:, 1].min() - pad
            x1, y1 = px[:, 0].max() + pad, px[:, 1].max() + pad
            out.append((int(max(0, x0)), int(max(0, y0)), int(x1 - x0), int(y1 - y0)))
    return out


def fix_auto(path, coat_xy, out=None, strength=1.0):
    arr = np.asarray(Image.open(path).convert("RGB"))
    boxes = auto_boxes(arr)
    if not boxes:
        raise ValueError("auto mode found no stark-white blobs in the lower frame")
    return fix_image(path, coat_xy=coat_xy, out=out, boxes=boxes, strength=strength), boxes


def preview_image(path, seeds=None, tol=TOL, sat_max=SAT_MAX, val_min=VAL_MIN, boxes=None):
    arr = np.asarray(Image.open(path).convert("RGB"))
    mask = np.zeros(arr.shape[:2], bool)
    if seeds:
        mask |= wand_mask(arr, seeds, tol, sat_max, val_min)
    if boxes:
        for (x, y, w, h) in boxes:
            c = arr[y:y+h, x:x+w].astype(np.float64)
            wgt, barrier, _, _ = _edgeaware_weight(c)
            m = _smoothstep(wgt, 0.12, 0.6) > 0.3
            m[barrier] = False
            mask[y:y+h, x:x+w] |= m
    if not mask.any():
        raise ValueError("empty selection — provide --seed and/or --box")
    ov = arr.copy(); ov[mask] = (0.35 * ov[mask] + 0.65 * np.array([255, 0, 200])).astype(np.uint8)
    out = os.path.splitext(path)[0] + "_wandmask.png"
    Image.fromarray(ov).save(out)
    return out, int(mask.sum())


def fix_video(path, rois, coat_xy, out=None, strength=1.0):
    """Per-frame edgeaware fix inside each ROI (coat re-sampled per frame -> tracks lighting)."""
    out = out or os.path.splitext(path)[0] + "_wand.mp4"
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=r_frame_rate", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip() or "24/1"
    with tempfile.TemporaryDirectory(prefix="wand_") as td:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, f"{td}/f%05d.png"], check=True)
        for fn in sorted(os.listdir(td)):
            fp = os.path.join(td, fn)
            arr = np.asarray(Image.open(fp).convert("RGB")).copy()
            coat = sample_coat(arr, coat_xy)
            for b in rois:
                _edgeaware_box(arr, b, coat, strength)
            Image.fromarray(arr).save(fp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", fps,
                        "-i", f"{td}/f%05d.png", "-c:v", "libx264", "-crf", "18",
                        "-pix_fmt", "yuv420p", out], check=True)
    return out


def _xy(s):
    x, y = s.split(","); return int(x), int(y)


def _roi(s):
    x, y, w, h = s.split(","); return int(x), int(y), int(w), int(h)


def main():
    ap = argparse.ArgumentParser(description="Magic Wand — zero-token local color-drift fixer")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("preview"); p.add_argument("image"); p.add_argument("--seed", type=_xy, action="append")
    p.add_argument("--box", type=_roi, action="append")
    p.add_argument("--tol", type=float, default=TOL); p.add_argument("--sat-max", type=float, default=SAT_MAX)
    p.add_argument("--val-min", type=float, default=VAL_MIN)
    f = sub.add_parser("fix"); f.add_argument("image"); f.add_argument("--seed", type=_xy, action="append")
    f.add_argument("--box", type=_roi, action="append"); f.add_argument("--coat", type=_xy, required=True)
    f.add_argument("--out"); f.add_argument("--strength", type=float, default=1.0)
    f.add_argument("--tol", type=float, default=TOL); f.add_argument("--sat-max", type=float, default=SAT_MAX)
    f.add_argument("--val-min", type=float, default=VAL_MIN)
    au = sub.add_parser("auto"); au.add_argument("image"); au.add_argument("--coat", type=_xy, required=True)
    au.add_argument("--out"); au.add_argument("--strength", type=float, default=1.0)
    v = sub.add_parser("fixvid"); v.add_argument("video"); v.add_argument("--roi", type=_roi, action="append", required=True)
    v.add_argument("--coat", type=_xy, required=True); v.add_argument("--out")
    v.add_argument("--strength", type=float, default=1.0)
    a = ap.parse_args()
    if a.cmd == "preview":
        out, n = preview_image(a.image, a.seed, a.tol, a.sat_max, a.val_min, boxes=a.box)
        print(f"mask {n}px -> {out}")
    elif a.cmd == "fix":
        out, n = fix_image(a.image, a.seed, a.coat, a.out, a.tol, a.sat_max, a.val_min,
                           boxes=a.box, strength=a.strength)
        print(f"fixed {n}px -> {out}")
    elif a.cmd == "auto":
        (out, n), boxes = fix_auto(a.image, a.coat, a.out, a.strength)
        print(f"auto boxes: {boxes}\nfixed {n}px -> {out}")
    else:
        print(f"fixed -> {fix_video(a.video, a.roi, a.coat, a.out, a.strength)}")


if __name__ == "__main__":
    main()
