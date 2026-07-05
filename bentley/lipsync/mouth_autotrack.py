"""Auto-generate a mouth track by template-matching Bentley's high-contrast black muzzle.

This is the labor-bottleneck killer (review amendment): hand keyframes become the exception.
numpy normalized cross-correlation on downscaled grayscale frames (no cv2 dependency); the
template is a user-selected muzzle crop from frame 0; the mouth anchor is a fixed offset from
the template hit, scaled by the match size. Emits a MouthTrack with one keyframe per sampled
frame (smoothed)."""
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from bentley.lipsync.mouth_track import MouthTrack


def _frames(video, fps, workdir):
    out = Path(workdir) / "at_frames"
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
                    "-vf", f"fps={fps}", str(out / "f_%05d.png")], check=True)
    return sorted(out.glob("f_*.png"))


def _gray(img, ds):
    a = np.asarray(img.convert("L"), dtype=np.float32)
    return a[::ds, ::ds]


def _ncc_best(frame, tpl, center=None, radius=None):
    """Best normalized-cross-correlation hit of tpl in frame -> (y, x, score). Brute force but
    downscaled; fine for 5s clips. center/radius (in downscaled px) restrict the search window —
    the head moves slowly, so a windowed search can't teleport to a look-alike blob (paw, tag)."""
    fh, fw = frame.shape
    th, tw = tpl.shape
    tz = (tpl - tpl.mean()) / (tpl.std() + 1e-6)
    y0, y1, x0, x1 = 0, fh - th, 0, fw - tw
    if center is not None and radius is not None:
        cy, cx = center
        y0, y1 = max(0, cy - radius), min(fh - th, cy + radius)
        x0, x1 = max(0, cx - radius), min(fw - tw, cx + radius)
    best = (y0, x0, -2.0)
    for y in range(y0, max(y0 + 1, y1), 2):
        for x in range(x0, max(x0 + 1, x1), 2):
            win = frame[y:y + th, x:x + tw]
            wz = (win - win.mean()) / (win.std() + 1e-6)
            s = float((tz * wz).mean())
            if s > best[2]:
                best = (y, x, s)
    return best


def autotrack(video, template_box, mouth_offset, fps=6, downscale=4, workdir=None, min_score=0.35,
              search_radius_px=70):
    """Track template_box=(x0,y0,x1,y1) (frame-0 pixel coords) through the clip.

    mouth_offset=(dx,dy) locates the mouth anchor relative to the template's top-left.
    Returns a MouthTrack (keyframes at 1/fps spacing, 3-tap smoothed). Frames whose best match
    scores under min_score keep the previous position (no jumps). search_radius_px windows each
    frame's search around the previous hit so the tracker can't jump to a distant look-alike."""
    wd = Path(workdir or tempfile.mkdtemp(prefix="autotrack_"))
    frames = _frames(video, fps, wd)
    if not frames:
        raise RuntimeError(f"no frames extracted from {video}")
    x0, y0, x1, y1 = template_box
    ds = downscale
    f0 = _gray(Image.open(frames[0]), ds)
    tpl = f0[y0 // ds:y1 // ds, x0 // ds:x1 // ds]
    base_w = tpl.shape[1]
    raw = []
    px, py = x0, y0
    rad = max(2, search_radius_px // ds)
    for i, fp in enumerate(frames):
        g = _gray(Image.open(fp), ds)
        by, bx, score = _ncc_best(g, tpl, center=(py // ds, px // ds), radius=rad)
        if score >= min_score:
            px, py = bx * ds, by * ds
        raw.append({"time": i / fps, "x": px + mouth_offset[0], "y": py + mouth_offset[1],
                    "scale": 1.0, "rotation_deg": 0.0, "visible": True, "score": round(score, 3)})
    # 3-tap moving-average smoothing (kills NCC jitter without lagging real motion)
    kf = []
    for i, k in enumerate(raw):
        win = raw[max(0, i - 1):i + 2]
        kf.append({**{kk: vv for kk, vv in k.items() if kk != "score"},
                   "x": sum(w["x"] for w in win) / len(win),
                   "y": sum(w["y"] for w in win) / len(win)})
    track = MouthTrack(kf)
    track.match_scores = [k["score"] for k in raw]
    track.template_width_px = base_w * ds
    return track
