"""v2 tracker: TWO-point tracking (nose + a second head feature) -> per-frame translation,
ROTATION and SCALE — so the mouth anchor follows the head's real geometry instead of a fixed
offset (v1's failure mode: head rotates/reframes -> fixed offset points at the cheek).

The mouth anchor is expressed in the local frame of the (p1 -> p2) vector at frame 0 and
re-projected through each frame's tracked pair. Also emits a per-frame angle proxy
(p1-p2 distance ratio vs frame 0) that the renderer uses to pick front/three-quarter/side sheets."""
import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from bentley.lipsync.mouth_track import MouthTrack


def _frames(video, fps, workdir):
    out = Path(workdir) / "at2_frames"
    out.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
                    "-vf", f"fps={fps}", str(out / "f_%05d.png")], check=True)
    return sorted(out.glob("f_*.png"))


def _gray(img, ds):
    return np.asarray(img.convert("L"), dtype=np.float32)[::ds, ::ds]


def _ncc_best(frame, tpl, cy=None, cx=None, radius=None):
    """Best NCC hit; optionally restricted to a window around (cy,cx) — faster and steadier."""
    fh, fw = frame.shape
    th, tw = tpl.shape
    tz = (tpl - tpl.mean()) / (tpl.std() + 1e-6)
    y0, y1, x0, x1 = 0, fh - th, 0, fw - tw
    if radius is not None and cy is not None:
        y0, y1 = max(0, cy - radius), min(fh - th, cy + radius)
        x0, x1 = max(0, cx - radius), min(fw - tw, cx + radius)
    best = (y0, x0, -2.0)
    for y in range(y0, max(y0 + 1, y1), 1):
        for x in range(x0, max(x0 + 1, x1), 1):
            win = frame[y:y + th, x:x + tw]
            wz = (win - win.mean()) / (win.std() + 1e-6)
            s = float((tz * wz).mean())
            if s > best[2]:
                best = (y, x, s)
    return best


def autotrack2(video, box1, box2, mouth_xy, fps=12, downscale=4, workdir=None, min_score=0.3,
               search_radius_px=90):
    """box1/box2: two rigid head features in frame-0 pixel coords (e.g. nose, eye).
    mouth_xy: the mouth anchor in frame-0 pixel coords. Returns a MouthTrack whose keyframes
    carry x/y/scale/rotation_deg + .angle_ratio (per-key p1-p2 length vs frame 0)."""
    wd = Path(workdir or tempfile.mkdtemp(prefix="autotrack2_"))
    frames = _frames(video, fps, wd)
    ds = downscale
    g0 = _gray(Image.open(frames[0]), ds)

    def tpl(box):
        x0, y0, x1, y1 = box
        return g0[y0 // ds:y1 // ds, x0 // ds:x1 // ds]

    t1, t2 = tpl(box1), tpl(box2)
    p1_0 = np.array([box1[0], box1[1]], float)
    p2_0 = np.array([box2[0], box2[1]], float)
    base = p2_0 - p1_0
    base_len = np.hypot(*base)
    # mouth anchor in the local (p1->p2) frame at t0
    m_rel = np.array(mouth_xy, float) - p1_0
    rad = search_radius_px // ds
    kf = []
    prev1 = (int(box1[1]) // ds, int(box1[0]) // ds)
    prev2 = (int(box2[1]) // ds, int(box2[0]) // ds)
    for i, fp in enumerate(frames):
        g = _gray(Image.open(fp), ds)
        y1_, x1_, s1 = _ncc_best(g, t1, prev1[0], prev1[1], rad)
        y2_, x2_, s2 = _ncc_best(g, t2, prev2[0], prev2[1], rad)
        if s1 >= min_score:
            prev1 = (y1_, x1_)
        if s2 >= min_score:
            prev2 = (y2_, x2_)
        p1 = np.array([prev1[1] * ds, prev1[0] * ds], float)
        p2 = np.array([prev2[1] * ds, prev2[0] * ds], float)
        v = p2 - p1
        vlen = max(1e-6, np.hypot(*v))
        rot = math.degrees(math.atan2(v[1], v[0]) - math.atan2(base[1], base[0]))
        scale = vlen / base_len
        # re-project the mouth anchor: rotate+scale m_rel by the frame's similarity transform
        cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
        m = p1 + scale * np.array([m_rel[0] * cr - m_rel[1] * sr,
                                   m_rel[0] * sr + m_rel[1] * cr])
        kf.append({"time": i / fps, "x": float(m[0]), "y": float(m[1]),
                   "scale": float(scale), "rotation_deg": float(rot), "visible": True,
                   "angle_ratio": float(scale and vlen / base_len),
                   "score": round(min(s1, s2), 3)})
    # 3-tap smoothing on position + rotation + scale
    sm = []
    for i, k in enumerate(kf):
        win = kf[max(0, i - 1):i + 2]
        avg = lambda key: sum(w[key] for w in win) / len(win)
        sm.append({"time": k["time"], "x": avg("x"), "y": avg("y"), "scale": avg("scale"),
                   "rotation_deg": avg("rotation_deg"), "visible": True,
                   "angle_ratio": avg("angle_ratio")})
    track = MouthTrack(sm)
    track.match_scores = [k["score"] for k in kf]
    return track
